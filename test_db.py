# test_db.py
from database import get_db_connection

def verify_onboarding_data():
    print("⏳ Querying Supabase/Postgres...")

    try:
        conn = get_db_connection()
        records = conn.execute(
            "SELECT * FROM businesses ORDER BY id DESC"
        ).fetchall()

        if not records:
            print("⚠️ 'businesses' table is empty.")
            return

        print(f"✅ Success! Found {len(records)} business record(s) stored in Postgres.\n")
        print("-" * 70)

        for row in records:
            print(f"📍 [Tenant ID {row['id']}] - {row['name']}")
            print(f"   Category:  {row['category']}")
            print(f"   Place ID:  {row['place_id']}")
            print(f"   Threshold: {row['threshold']} Stars")
            print(f"   Alert to:  {row['primary_alert']}")
            print(f"   Registered: {row['created_at']}")
            print("-" * 70)

        conn.close()

    except Exception as e:
        print(f"❌ Internal Test Failure: {str(e)}")

if __name__ == "__main__":
    verify_onboarding_data()
