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
from models import create_admin, get_admin_by_username

# ── Template & static folders live inside frontend/ ─────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR  = os.path.join(BASE_DIR, "..", "frontend", "templates")
STATIC_DIR    = os.path.join(BASE_DIR, "..", "frontend", "static")

app = Flask(
    __name__,
    template_folder=os.path.abspath(TEMPLATE_DIR),
    static_folder=os.path.abspath(STATIC_DIR),
)

app.secret_key = os.environ.get("SECRET_KEY", "schemo-super-secret-key-2024")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# ── Register blueprint (routes) ──────────────────────────────────────────
from routes import bp
app.register_blueprint(bp)


# ── Bootstrap default admin on first start ──────────────────────────────
def seed_admin():
    """Create a default admin account if none exists yet."""
    if not get_admin_by_username("admin"):
        create_admin("admin", "admin123")
        print("[Schemo] Default admin created  →  username: admin | password: admin123")


if __name__ == "__main__":
    try:
        seed_admin()
    except Exception as e:
        print(f"[WARN] Could not seed admin (DB might not be ready): {e}")
    app.run(debug=True, host="0.0.0.0", port=5000)
