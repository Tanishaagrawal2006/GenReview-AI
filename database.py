"""
database.py — Supabase / Postgres data layer.

This module used to talk to a local SQLite file, which is why Render's
dashboard and QR/URL data kept "disappearing": Render's disk is ephemeral,
so reviewflow.db was reset on every redeploy or restart.

It now talks to Postgres (Supabase), which persists independently of Render.

IMPORTANT: The public interface (get_db_connection, conn.execute(...),
conn.cursor(), cursor.lastrowid, .fetchone(), .fetchall(), .commit(),
.close()) is kept identical to the old sqlite3 interface on purpose, so
app.py and rag_engine.py did not need to be rewritten. Under the hood it
now runs against Postgres.
"""

import os
import re
import psycopg2
import psycopg2.extras

_INSERT_RE = re.compile(r"^\s*INSERT\s+INTO", re.IGNORECASE)

def _raw_connect():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Set it to your Supabase connection string "
            "(Project Settings -> Database -> Connection string -> URI, e.g. "
            "postgresql://postgres:[password]@[host]:5432/postgres) as an "
            "environment variable, both locally (.env) and on Render "
            "(Environment tab)."
        )
    return psycopg2.connect(db_url, cursor_factory=psycopg2.extras.RealDictCursor)


class _CursorWrapper:
    """Mimics sqlite3.Cursor closely enough for this codebase's needs:
    execute() / fetchone() / fetchall() / lastrowid, with '?' placeholders."""

    def __init__(self, pg_cursor):
        self._cur = pg_cursor
        self.lastrowid = None

    def execute(self, sql, params=()):
        pg_sql = sql.replace("?", "%s")

        # sqlite3.Cursor.lastrowid has no direct Postgres equivalent, so for
        # INSERT statements we transparently append RETURNING id (every
        # table here has an `id` primary key) and capture it ourselves.
        is_insert = bool(_INSERT_RE.match(pg_sql))
        if is_insert and "returning" not in pg_sql.lower():
            pg_sql = pg_sql.rstrip().rstrip(";") + " RETURNING id"

        self._cur.execute(pg_sql, params)

        if is_insert:
            try:
                row = self._cur.fetchone()
                self.lastrowid = row["id"] if row else None
            except psycopg2.ProgrammingError:
                self.lastrowid = None
        return self

    def fetchone(self):
        return self._cur.fetchone()

    def fetchall(self):
        return self._cur.fetchall()

    def __iter__(self):
        return iter(self._cur)


class _ConnectionWrapper:
    """Mimics the subset of sqlite3.Connection this codebase relies on."""

    def __init__(self, pg_conn):
        self._conn = pg_conn

    def cursor(self):
        return _CursorWrapper(self._conn.cursor())

    def execute(self, sql, params=()):
        # sqlite3.Connection.execute() is shorthand for cursor().execute()
        return self.cursor().execute(sql, params)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()


def get_db_connection():
    return _ConnectionWrapper(_raw_connect())


def init_db():
    """Creates tables if they don't exist yet (idempotent, safe to run on
    every boot) and seeds the default super_admin account. Mirrors
    supabase_schema.sql — keep the two in sync if you change one."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS businesses (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            custom_category TEXT,
            place_id TEXT NOT NULL,
            threshold REAL NOT NULL DEFAULT 4.0,
            primary_alert TEXT NOT NULL,
            alternate_alert TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id SERIAL PRIMARY KEY,
            business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            must_change_password INTEGER DEFAULT 1
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS feedback_records (
            id SERIAL PRIMARY KEY,
            business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
            overall_rating INTEGER NOT NULL,
            sub_rating_1 INTEGER,
            sub_rating_2 INTEGER,
            complaint_text TEXT,
            improvement_tags TEXT,
            customer_contact TEXT,
            selected_draft_text TEXT,
            is_read INTEGER DEFAULT 0,
            status TEXT DEFAULT 'New',
            is_visible INTEGER DEFAULT 1,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS business_knowledge (
            id SERIAL PRIMARY KEY,
            business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
            source_type TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS fingerprints (
            id SERIAL PRIMARY KEY,
            business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
            device_hash TEXT NOT NULL,
            last_scanned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(business_id, device_hash)
        )
    ''')

    from werkzeug.security import generate_password_hash
    cur.execute(
        "INSERT INTO accounts (username, password, role, must_change_password) "
        "VALUES (?, ?, ?, 0) ON CONFLICT (username) DO NOTHING",
        ('dbs_admin', generate_password_hash('dbs_secure2026'), 'super_admin')
    )

    conn.commit()
    conn.close()
    print("🚀 Database (Postgres/Supabase) schema verified and ready.")
