"""
models.py  –  All database queries (User + Scheme + Admin)
Uses Supabase Python client. All function signatures kept identical.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from database import supabase


# ═══════════════════════════════════════════════════════════════
#  USER MODEL
# ═══════════════════════════════════════════════════════════════

def create_user(name, email, phone_number, password, age, gender, community, occupation, state):
    """Insert a new user. Returns new user id."""
    hashed = generate_password_hash(password)
    res = supabase.table("users").insert({
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "password": hashed,
        "age": age,
        "gender": gender,
        "community": community,
        "occupation": occupation,
        "state": state,
    }).execute()
    return res.data[0]["id"] if res.data else None


def get_user_by_email(email):
    """Return user dict or None."""
    res = supabase.table("users").select("*").eq("email", email).limit(1).execute()
    return res.data[0] if res.data else None


def get_or_create_google_user(name, email):
    """Find user by email. If not found, create a minimal user with Google data."""
    user = get_user_by_email(email)
    if user:
        return user

    import uuid, random
    dummy_phone = "G" + str(random.randint(100000000, 999999999))
    dummy_pw = str(uuid.uuid4())

    user_id = create_user(
        name=name, email=email, phone_number=dummy_phone,
        password=dummy_pw, age=0, gender="Other",
        community="General", occupation="Other", state="Not Specified"
    )
    return get_user_by_id(user_id)


def get_user_by_phone(phone):
    """Return user dict or None."""
    res = supabase.table("users").select("*").eq("phone_number", phone).limit(1).execute()
    return res.data[0] if res.data else None


def get_user_by_id(user_id):
    """Return user dict or None."""
    res = supabase.table("users").select("*").eq("id", user_id).limit(1).execute()
    return res.data[0] if res.data else None


def verify_user_password(user, raw_password):
    """Check a plaintext password against the stored hash."""
    return check_password_hash(user["password"], raw_password)


def get_all_users():
    """Return list of all registered users (no passwords)."""
    res = supabase.table("users").select(
        "id, name, email, phone_number, age, gender, community, occupation, state, created_at"
    ).order("created_at", desc=True).execute()
    return res.data or []


def delete_user(user_id):
    """Delete a user by id."""
    supabase.table("users").delete().eq("id", user_id).execute()


def update_user(user_id, age, gender, community, occupation, state, name=None):
    """Update user profile fields."""
    payload = {
        "age": int(age),
        "gender": gender,
        "community": community,
        "occupation": occupation,
        "state": state,
    }
    if name:
        payload["name"] = name
    supabase.table("users").update(payload).eq("id", user_id).execute()


def update_user_password(user_id, new_password):
    """Update hashed password for a user."""
    hashed = generate_password_hash(new_password)
    supabase.table("users").update({"password": hashed}).eq("id", user_id).execute()


def get_user_stats():
    """Returns analytics data (totals, occupation, gender, community, timeline, trends)."""
    from datetime import datetime, timedelta

    all_users = supabase.table("users").select(
        "id, gender, community, occupation, created_at"
    ).execute().data or []

    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    two_weeks_ago = now - timedelta(days=14)

    def parse_dt(s):
        if not s:
            return None
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
        except Exception:
            return None

    def calc_trend(curr, prev):
        if prev == 0:
            return 0 if curr == 0 else 100
        return round(((curr - prev) / prev) * 100)

    current_week = [u for u in all_users if parse_dt(u.get("created_at")) and parse_dt(u["created_at"]) >= week_ago]
    prev_week    = [u for u in all_users if parse_dt(u.get("created_at")) and two_weeks_ago <= parse_dt(u["created_at"]) < week_ago]

    def count_by(lst, key, val):
        return sum(1 for u in lst if u.get(key) == val)

    working_occ = {"Salaried Employee", "Self Employed", "Business Owner"}

    totals = {
        "total":    len(all_users),
        "female":   count_by(all_users, "gender", "Female"),
        "male":     count_by(all_users, "gender", "Male"),
        "students": count_by(all_users, "occupation", "Student"),
        "working":  sum(1 for u in all_users if u.get("occupation") in working_occ),
    }
    trends = {
        "total":    calc_trend(len(current_week), len(prev_week)),
        "female":   calc_trend(count_by(current_week, "gender", "Female"), count_by(prev_week, "gender", "Female")),
        "male":     calc_trend(count_by(current_week, "gender", "Male"), count_by(prev_week, "gender", "Male")),
        "students": calc_trend(count_by(current_week, "occupation", "Student"), count_by(prev_week, "occupation", "Student")),
        "working":  calc_trend(
            sum(1 for u in current_week if u.get("occupation") in working_occ),
            sum(1 for u in prev_week if u.get("occupation") in working_occ),
        ),
    }

    # Group by occupation
    occ_counts = {}
    for u in all_users:
        k = u.get("occupation", "Other")
        occ_counts[k] = occ_counts.get(k, 0) + 1
    occupations = [{"label": k, "count": v} for k, v in occ_counts.items()]

    # Group by gender
    gen_counts = {}
    for u in all_users:
        k = u.get("gender", "Other")
        gen_counts[k] = gen_counts.get(k, 0) + 1
    genders = [{"label": k, "count": v} for k, v in gen_counts.items()]

    # Group by community
    com_counts = {}
    for u in all_users:
        k = u.get("community", "General")
        com_counts[k] = com_counts.get(k, 0) + 1
    communities = [{"label": k, "count": v} for k, v in com_counts.items()]

    # Activity by date (last 14 days)
    day_counts = {}
    for u in all_users:
        dt = parse_dt(u.get("created_at"))
        if dt and dt >= two_weeks_ago:
            day = dt.strftime("%Y-%m-%d")
            day_counts[day] = day_counts.get(day, 0) + 1
    activity = [{"label": k, "count": v} for k, v in sorted(day_counts.items())]

    return {
        "totals": totals, "trends": trends,
        "occupations": occupations, "genders": genders,
        "communities": communities, "activity": activity,
    }


# ═══════════════════════════════════════════════════════════════
#  SCHEME MODEL
# ═══════════════════════════════════════════════════════════════

def get_all_schemes():
    """Return all schemes ordered by name."""
    res = supabase.table("schemes").select("*").order("scheme_name").execute()
    return res.data or []


def get_scheme_by_id(scheme_id):
    """Return a single scheme dict or None."""
    res = supabase.table("schemes").select("*").eq("id", scheme_id).limit(1).execute()
    return res.data[0] if res.data else None


def get_eligible_schemes(user):
    """
    Return schemes where community matches (or is 'All'),
    age is within [min_age, max_age], and income <= max_income.
    Filtering done in Python since Supabase doesn't support FIND_IN_SET.
    """
    res = supabase.table("schemes").select("*").execute()
    all_schemes = res.data or []

    user_community = user.get("community", "")
    user_age       = int(user.get("age", 0))
    user_income    = float(user.get("income", 0))

    eligible = []
    for s in all_schemes:
        # Community check
        communities = [c.strip() for c in s.get("community", "").split(",")]
        if "All" not in communities and user_community not in communities:
            continue
        # Age check
        if not (s.get("min_age", 0) <= user_age <= s.get("max_age", 100)):
            continue
        # Income check (0 = no limit)
        max_inc = float(s.get("max_income", 0))
        if max_inc != 0 and user_income > max_inc:
            continue
        eligible.append(s)

    eligible.sort(key=lambda x: x.get("scheme_name", ""))
    return eligible


def add_scheme(name, description, eligibility, community, min_age, max_age,
               max_income, benefits, documents, deadline, link):
    res = supabase.table("schemes").insert({
        "scheme_name": name,
        "description": description,
        "eligibility": eligibility,
        "community": community,
        "min_age": min_age,
        "max_age": max_age,
        "max_income": max_income,
        "benefits": benefits,
        "documents_required": documents,
        "deadline": deadline if deadline else None,
        "official_link": link,
    }).execute()
    return res.data[0]["id"] if res.data else None


def update_scheme(scheme_id, name, description, eligibility, community, min_age, max_age,
                  max_income, benefits, documents, deadline, link):
    supabase.table("schemes").update({
        "scheme_name": name,
        "description": description,
        "eligibility": eligibility,
        "community": community,
        "min_age": min_age,
        "max_age": max_age,
        "max_income": max_income,
        "benefits": benefits,
        "documents_required": documents,
        "deadline": deadline if deadline else None,
        "official_link": link,
    }).eq("id", scheme_id).execute()


def delete_scheme(scheme_id):
    supabase.table("schemes").delete().eq("id", scheme_id).execute()


# ═══════════════════════════════════════════════════════════════
#  ADMIN MODEL
# ═══════════════════════════════════════════════════════════════

def get_admin_by_username(username):
    res = supabase.table("admins").select("*").eq("username", username).limit(1).execute()
    return res.data[0] if res.data else None


def verify_admin_password(admin, raw_password):
    return check_password_hash(admin["password"], raw_password)


def create_admin(username, password):
    hashed = generate_password_hash(password)
    try:
        supabase.table("admins").insert({"username": username, "password": hashed}).execute()
        return True
    except Exception:
        return False  # already exists
