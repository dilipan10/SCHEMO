"""
routes.py  –  All Flask URL routes for Schemo
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash
)
from functools import wraps
import models

bp = Blueprint("main", __name__)


# ─── Decorators ────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access that page.", "warning")
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("main.admin_login"))
        return f(*args, **kwargs)
    return wrapper


# ─── Public routes ─────────────────────────────────────────────

@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/schemes")
def schemes():
    all_schemes = models.get_all_schemes()
    return render_template("schemes.html", schemes=all_schemes)


# ─── Auth routes ───────────────────────────────────────────────

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        name       = request.form.get("name", "").strip()
        email      = request.form.get("email", "").strip().lower()
        password   = request.form.get("password", "")
        age        = request.form.get("age", 0)
        gender     = request.form.get("gender", "")
        community  = request.form.get("community", "")
        occupation = request.form.get("occupation", "").strip()
        state      = request.form.get("state", "").strip()

        # Basic validation
        if not all([name, email, password, age, gender, community, occupation, state]):
            flash("All fields are required.", "danger")
            return render_template("signup.html")

        if models.get_user_by_email(email):
            flash("An account with this email already exists. Please log in.", "warning")
            return render_template("signup.html")

        try:
            models.create_user(name, email, password, int(age), gender,
                               community, occupation, state)
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("main.login"))
        except Exception as e:
            flash(f"Registration failed: {e}", "danger")

    return render_template("signup.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = models.get_user_by_email(email)
        if user and models.verify_user_password(user, password):
            session["user_id"]   = user["id"]
            session["user_name"] = user["name"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


# ─── User Dashboard ─────────────────────────────────────────────

@bp.route("/dashboard")
@login_required
def dashboard():
    user = models.get_user_by_id(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("main.login"))
    eligible = models.get_eligible_schemes(user)
    return render_template("dashboard.html", user=user, schemes=eligible)


# ─── Admin Auth ────────────────────────────────────────────────

@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("is_admin"):
        return redirect(url_for("main.admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = models.get_admin_by_username(username)
        if admin and models.verify_admin_password(admin, password):
            session["is_admin"]      = True
            session["admin_username"] = admin["username"]
            flash("Admin login successful.", "success")
            return redirect(url_for("main.admin_dashboard"))
        else:
            flash("Invalid admin credentials.", "danger")

    return render_template("admin_login.html")


@bp.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    session.pop("admin_username", None)
    flash("Admin logged out.", "info")
    return redirect(url_for("main.index"))


# ─── Admin Dashboard ─────────────────────────────────────────────

@bp.route("/admin")
@bp.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    users   = models.get_all_users()
    schemes = models.get_all_schemes()
    return render_template("admin.html", users=users, schemes=schemes)


# ─── Admin – Delete user ────────────────────────────────────────

@bp.route("/admin/user/delete/<int:user_id>", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    models.delete_user(user_id)
    flash("User deleted successfully.", "success")
    return redirect(url_for("main.admin_dashboard"))


# ─── Admin – Add scheme ─────────────────────────────────────────

@bp.route("/admin/scheme/add", methods=["GET", "POST"])
@admin_required
def admin_add_scheme():
    if request.method == "POST":
        try:
            models.add_scheme(
                name        = request.form["scheme_name"].strip(),
                description = request.form["description"].strip(),
                eligibility = request.form["eligibility"].strip(),
                community   = request.form["community"].strip(),
                min_age     = int(request.form.get("min_age", 0)),
                max_age     = int(request.form.get("max_age", 100)),
                max_income  = float(request.form.get("max_income", 0)),
                benefits    = request.form["benefits"].strip(),
                documents   = request.form["documents_required"].strip(),
                deadline    = request.form.get("deadline", "").strip() or None,
                link        = request.form["official_link"].strip(),
            )
            flash("Scheme added successfully.", "success")
        except Exception as e:
            flash(f"Error adding scheme: {e}", "danger")
        return redirect(url_for("main.admin_dashboard"))
    return render_template("scheme_form.html", scheme=None, action="Add")


# ─── Admin – Edit scheme ─────────────────────────────────────────

@bp.route("/admin/scheme/edit/<int:scheme_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_scheme(scheme_id):
    scheme = models.get_scheme_by_id(scheme_id)
    if not scheme:
        flash("Scheme not found.", "warning")
        return redirect(url_for("main.admin_dashboard"))

    if request.method == "POST":
        try:
            models.update_scheme(
                scheme_id   = scheme_id,
                name        = request.form["scheme_name"].strip(),
                description = request.form["description"].strip(),
                eligibility = request.form["eligibility"].strip(),
                community   = request.form["community"].strip(),
                min_age     = int(request.form.get("min_age", 0)),
                max_age     = int(request.form.get("max_age", 100)),
                max_income  = float(request.form.get("max_income", 0)),
                benefits    = request.form["benefits"].strip(),
                documents   = request.form["documents_required"].strip(),
                deadline    = request.form.get("deadline", "").strip() or None,
                link        = request.form["official_link"].strip(),
            )
            flash("Scheme updated successfully.", "success")
        except Exception as e:
            flash(f"Error updating scheme: {e}", "danger")
        return redirect(url_for("main.admin_dashboard"))
    return render_template("scheme_form.html", scheme=scheme, action="Edit")


# ─── Admin – Delete scheme ────────────────────────────────────────

@bp.route("/admin/scheme/delete/<int:scheme_id>", methods=["POST"])
@admin_required
def admin_delete_scheme(scheme_id):
    models.delete_scheme(scheme_id)
    flash("Scheme deleted successfully.", "success")
    return redirect(url_for("main.admin_dashboard"))
