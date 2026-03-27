"""
app.py  –  Entry point for Schemo Flask App
---------------------------------------------------------------------------
Run with:  python app.py
---------------------------------------------------------------------------
"""

import sys
import os
from dotenv import load_dotenv

# Load .env variables (GEMINI_API_KEY etc.)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Make backend/ importable when running app.py from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from flask import Flask
from models import create_admin, get_admin_by_username, get_all_schemes, add_scheme

# ── Template & static folders live inside frontend/ ─────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR  = os.path.join(BASE_DIR, "..", "frontend", "templates")
STATIC_DIR    = os.path.join(BASE_DIR, "..", "frontend", "static")

app = Flask(
    __name__,
    template_folder=os.path.abspath(TEMPLATE_DIR),
    static_folder=os.path.abspath(STATIC_DIR),
)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "schemo-super-secret-key-2024")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["CLERK_PUBLISHABLE_KEY"] = os.environ.get("CLERK_PUBLISHABLE_KEY", "")

# ── Register blueprint (routes) ──────────────────────────────────────────
from routes import bp
app.register_blueprint(bp)

from routes import register_error_handlers
register_error_handlers(app)


# ── Bootstrap default admin ──────────────────────────────────────────────
def seed_admin():
    """Create admin from .env credentials (ADMIN_USERNAME / ADMIN_PASSWORD)."""
    username = os.environ.get("ADMIN_USERNAME", "admin")
    password = os.environ.get("ADMIN_PASSWORD", "admin123")
    if not get_admin_by_username(username):
        create_admin(username, password)
        print(f"[Schemo] Admin created  →  username: {username}")


# ── Auto-load schemes CSV on first run ───────────────────────────────────
def seed_schemes():
    """Load schemes_dataset.csv into Supabase if the schemes table is empty."""
    import csv
    existing = get_all_schemes()
    if existing:
        print(f"[Schemo] Schemes already loaded ({len(existing)} found) — skipping CSV seed.")
        return

    csv_path = os.path.join(BASE_DIR, "..", "database", "schemes_dataset.csv")
    if not os.path.exists(csv_path):
        print("[Schemo] schemes_dataset.csv not found — skipping seed.")
        return

    added = 0
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                add_scheme(
                    name        = row["scheme_name"].strip(),
                    description = row.get("description", "").strip(),
                    eligibility = row.get("eligibility", "").strip(),
                    community   = row.get("community", "All").strip(),
                    min_age     = int(row.get("min_age", 0) or 0),
                    max_age     = int(row.get("max_age", 100) or 100),
                    max_income  = float(row.get("max_income", 0) or 0),
                    benefits    = row.get("benefits", "").strip(),
                    documents   = row.get("documents_required", "").strip(),
                    deadline    = row.get("deadline", "").strip() or None,
                    link        = row.get("official_link", "").strip(),
                )
                added += 1
            except Exception as e:
                print(f"[Schemo] CSV seed error on row '{row.get('scheme_name')}': {e}")

    print(f"[Schemo] Seeded {added} schemes from CSV.")

# Run on startup (works for both gunicorn and direct run)
try:
    seed_admin()
except Exception as e:
    print(f"[WARN] Could not seed admin: {e}")

try:
    seed_schemes()
except Exception as e:
    print(f"[WARN] Could not seed schemes: {e}")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
