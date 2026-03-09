"""
models.py  –  All database queries (User + Scheme + Admin)
"""

from werkzeug.security import generate_password_hash, check_password_hash
from database import execute_query


# ═══════════════════════════════════════════════════════════════
#  USER MODEL
# ═══════════════════════════════════════════════════════════════

def create_user(name, email, password, age, gender, community, occupation, state):
    """Insert a new user. Returns new user id."""
    hashed = generate_password_hash(password)
    sql = """
        INSERT INTO users (name, email, password, age, gender, community, occupation, state)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(sql, (name, email, hashed, age, gender, community, occupation, state))


def get_user_by_email(email):
    """Return user dict or None."""
    sql = "SELECT * FROM users WHERE email = %s LIMIT 1"
    rows = execute_query(sql, (email,), fetch=True)
    return rows[0] if rows else None


def get_user_by_id(user_id):
    """Return user dict or None."""
    sql = "SELECT * FROM users WHERE id = %s LIMIT 1"
    rows = execute_query(sql, (user_id,), fetch=True)
    return rows[0] if rows else None


def verify_user_password(user, raw_password):
    """Check a plaintext password against the stored hash."""
    return check_password_hash(user["password"], raw_password)


def get_all_users():
    """Return list of all registered users (no passwords)."""
    sql = "SELECT id, name, email, age, gender, community, occupation, state, created_at FROM users ORDER BY created_at DESC"
    return execute_query(sql, fetch=True)


def delete_user(user_id):
    """Delete a user by id."""
    execute_query("DELETE FROM users WHERE id = %s", (user_id,))


# ═══════════════════════════════════════════════════════════════
#  SCHEME MODEL
# ═══════════════════════════════════════════════════════════════

def get_all_schemes():
    """Return all schemes ordered by name."""
    return execute_query("SELECT * FROM schemes ORDER BY scheme_name", fetch=True)


def get_scheme_by_id(scheme_id):
    """Return a single scheme dict or None."""
    rows = execute_query("SELECT * FROM schemes WHERE id = %s LIMIT 1", (scheme_id,), fetch=True)
    return rows[0] if rows else None


def get_eligible_schemes(user):
    """
    Return schemes where:
      - community matches user's community or is 'All'
      - user age is within [min_age, max_age]
      - user income is <= max_income  (0 in db = no limit)
    """
    sql = """
        SELECT * FROM schemes
        WHERE (community = 'All'
               OR FIND_IN_SET(%s, REPLACE(community, ', ', ',')) > 0
               OR FIND_IN_SET(%s, REPLACE(community, ' ', '')) > 0)
          AND min_age  <= %s
          AND max_age  >= %s
          AND (max_income = 0 OR max_income >= %s)
        ORDER BY scheme_name
    """
    params = (
        user["community"], user["community"],
        user["age"], user["age"],
        user.get("income", 0),
    )
    return execute_query(sql, params, fetch=True)


def add_scheme(name, description, eligibility, community, min_age, max_age,
               max_income, benefits, documents, deadline, link):
    sql = """
        INSERT INTO schemes
            (scheme_name, description, eligibility, community, min_age, max_age,
             max_income, benefits, documents_required, deadline, official_link)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    deadline = deadline if deadline else None
    return execute_query(sql, (name, description, eligibility, community, min_age, max_age,
                               max_income, benefits, documents, deadline, link))


def update_scheme(scheme_id, name, description, eligibility, community, min_age, max_age,
                  max_income, benefits, documents, deadline, link):
    sql = """
        UPDATE schemes SET
            scheme_name=%s, description=%s, eligibility=%s, community=%s,
            min_age=%s, max_age=%s, max_income=%s, benefits=%s,
            documents_required=%s, deadline=%s, official_link=%s
        WHERE id=%s
    """
    deadline = deadline if deadline else None
    execute_query(sql, (name, description, eligibility, community, min_age, max_age,
                        max_income, benefits, documents, deadline, link, scheme_id))


def delete_scheme(scheme_id):
    execute_query("DELETE FROM schemes WHERE id = %s", (scheme_id,))


# ═══════════════════════════════════════════════════════════════
#  ADMIN MODEL
# ═══════════════════════════════════════════════════════════════

def get_admin_by_username(username):
    rows = execute_query("SELECT * FROM admins WHERE username = %s LIMIT 1",
                         (username,), fetch=True)
    return rows[0] if rows else None


def verify_admin_password(admin, raw_password):
    return check_password_hash(admin["password"], raw_password)


def create_admin(username, password):
    hashed = generate_password_hash(password)
    try:
        execute_query("INSERT INTO admins (username, password) VALUES (%s, %s)",
                      (username, hashed))
        return True
    except Exception:
        return False   # already exists
