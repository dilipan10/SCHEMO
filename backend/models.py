"""
models.py  –  All database queries (User + Scheme + Admin)
"""

from werkzeug.security import generate_password_hash, check_password_hash
from database import execute_query


# ═══════════════════════════════════════════════════════════════
#  USER MODEL
# ═══════════════════════════════════════════════════════════════

def create_user(name, email, phone_number, password, age, gender, community, occupation, state):
    """Insert a new user. Returns new user id."""
    hashed = generate_password_hash(password)
    sql = """
        INSERT INTO users (name, email, phone_number, password, age, gender, community, occupation, state)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return execute_query(sql, (name, email, phone_number, hashed, age, gender, community, occupation, state))


def get_user_by_email(email):
    """Return user dict or None."""
    sql = "SELECT * FROM users WHERE email = %s LIMIT 1"
    rows = execute_query(sql, (email,), fetch=True)
    return rows[0] if rows else None


def get_user_by_phone(phone):
    """Return user dict or None."""
    sql = "SELECT * FROM users WHERE phone_number = %s LIMIT 1"
    rows = execute_query(sql, (phone,), fetch=True)
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
    sql = "SELECT id, name, email, phone_number, age, gender, community, occupation, state, created_at FROM users ORDER BY created_at DESC"
    return execute_query(sql, fetch=True)


def delete_user(user_id):
    """Delete a user by id."""
    execute_query("DELETE FROM users WHERE id = %s", (user_id,))


def get_user_stats():
    """Returns analytics data (totals, occupation, gender, community, timeline, trends)."""
    totals = {}
    trends = {}

    def get_count(sql_part):
        res = execute_query(f"SELECT COUNT(*) as c FROM users WHERE {sql_part}", fetch=True)
        return res[0]['c'] if res else 0

    def calc_trend_val(curr, prev):
        if prev == 0:
            return 0 if curr == 0 else 100
        return round(((curr - prev) / prev) * 100)

    # Time filters
    now_q = "AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)"
    prev_q = "AND created_at < DATE_SUB(NOW(), INTERVAL 7 DAY) AND created_at >= DATE_SUB(NOW(), INTERVAL 14 DAY)"

    # 1. Total Users
    totals['total'] = get_count("1=1")
    trends['total'] = calc_trend_val(get_count("1=1 " + now_q), get_count("1=1 " + prev_q))

    # 2. Female
    totals['female'] = get_count("gender = 'Female'")
    trends['female'] = calc_trend_val(get_count("gender = 'Female' " + now_q), get_count("gender = 'Female' " + prev_q))

    # 3. Male
    totals['male'] = get_count("gender = 'Male'")
    trends['male'] = calc_trend_val(get_count("gender = 'Male' " + now_q), get_count("gender = 'Male' " + prev_q))

    # 4. Students
    totals['students'] = get_count("occupation = 'Student'")
    trends['students'] = calc_trend_val(get_count("occupation = 'Student' " + now_q), get_count("occupation = 'Student' " + prev_q))

    # 5. Working Pros
    working_where = "occupation IN ('Salaried Employee', 'Self Employed', 'Business Owner')"
    totals['working'] = get_count(working_where)
    trends['working'] = calc_trend_val(get_count(working_where + " " + now_q), get_count(working_where + " " + prev_q))

    # Groupings
    occupations = execute_query("SELECT occupation as label, COUNT(*) as count FROM users GROUP BY occupation", fetch=True)
    genders = execute_query("SELECT gender as label, COUNT(*) as count FROM users GROUP BY gender", fetch=True)
    communities = execute_query("SELECT community as label, COUNT(*) as count FROM users GROUP BY community", fetch=True)
    activity = execute_query("SELECT DATE(created_at) as label, COUNT(*) as count FROM users GROUP BY DATE(created_at) ORDER BY label ASC LIMIT 14", fetch=True)

    return {
        "totals": totals,
        "trends": trends,
        "occupations": occupations,
        "genders": genders,
        "communities": communities,
        "activity": activity
    }


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

