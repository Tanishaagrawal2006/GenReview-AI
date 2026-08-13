"""
ReviewFlow — QR Code Regeneration Script
=========================================
Run this AFTER updating BASE_URL in .env to a real HTTPS URL.

Usage (from the reviewflow_app/ inner directory):
    python scripts/regenerate_qr.py

What it does:
    • Reads every business from the database
    • Calls generate_beautified_qr() for each one
    • Overwrites static/qr_codes/tenant_<id>.png with the new URL baked in

Prerequisites:
    • .env must have BASE_URL set to a valid public HTTPS URL
    • qrcode, Pillow must be installed (pip install qrcode pillow)
"""

import os
import sys

# Ensure we can import from the parent directory (app modules)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from dotenv import load_dotenv
load_dotenv(os.path.join(parent_dir, ".env"))

base_url = os.getenv("BASE_URL", "")
if not base_url or "127.0.0.1" in base_url or "YOUR_NGROK" in base_url:
    print("=" * 60)
    print("❌  ABORTED: BASE_URL is not set to a valid HTTPS URL.")
    print(f"   Current value: {base_url!r}")
    print()
    print("   Fix: open .env and set BASE_URL to your real domain,")
    print("   e.g.:  BASE_URL=\"https://abcd-1234.ngrok-free.app\"")
    print("=" * 60)
    sys.exit(1)

from database import get_db_connection
from qr_engine import generate_beautified_qr

print(f"\n🔄  Regenerating QR codes with BASE_URL = {base_url!r}\n")

conn = get_db_connection()
businesses = conn.execute("SELECT id, name, category, custom_category FROM businesses ORDER BY id").fetchall()
conn.close()

if not businesses:
    print("⚠️  No businesses found in the database. Nothing to regenerate.")
    sys.exit(0)

success = 0
errors  = 0

for biz in businesses:
    try:
        path = generate_beautified_qr(
            business_id=biz["id"],
            business_name=biz["name"],
            category=biz["category"],
            custom_category=biz["custom_category"]
        )
        print(f"  ✅  Business #{biz['id']:>3}  {biz['name'][:40]:<40}  →  {path}")
        success += 1
    except Exception as e:
        print(f"  ❌  Business #{biz['id']:>3}  {biz['name'][:40]:<40}  ERROR: {e}")
        errors += 1

print()
print(f"Done: {success} regenerated, {errors} errors.")
if errors == 0:
    print("✨  All QR codes are now pointing at your new URL. Download fresh copies from the owner dashboard.")
