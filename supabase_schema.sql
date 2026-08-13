-- SQL DDL for ReviewFlow AI tables in Supabase

-- 1. Businesses Table
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
);

-- 2. Accounts Table
CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    must_change_password INTEGER DEFAULT 1
);

-- 3. Feedback Records Table
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
);

-- 4. Business Knowledge Table
CREATE TABLE IF NOT EXISTS business_knowledge (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Device Fingerprints Table
CREATE TABLE IF NOT EXISTS fingerprints (
    id SERIAL PRIMARY KEY,
    business_id INTEGER REFERENCES businesses(id) ON DELETE CASCADE,
    device_hash TEXT NOT NULL,
    last_scanned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(business_id, device_hash)
);
