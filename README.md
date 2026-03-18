# Schemo – Government Scheme Aggregator Portal

> A full-stack Flask + MySQL web application where Indian citizens can register, log in, and discover government welfare schemes they are eligible for.

---

## 📁 Project Structure

```
schemo/
├── backend/
│   ├── app.py          ← Flask entry point (run this)
│   ├── routes.py       ← All URL routes (Blueprint)
│   ├── models.py       ← Database query functions
│   └── database.py     ← MySQL connection utility
│
├── frontend/
│   ├── templates/
│   │   ├── base.html         ← Shared layout (glassmorphic navbar, footer, toasts)
│   │   ├── index.html        ← Landing page (hero, features, how-it-works, CTA)
│   │   ├── signup.html       ← User registration (split layout, sticky info panel)
│   │   ├── login.html        ← User login (split layout with benefit panel)
│   │   ├── dashboard.html    ← User dashboard (stat cards + eligible schemes)
│   │   ├── schemes.html      ← Public schemes listing (glass cards + filter bar)
│   │   ├── admin_login.html  ← Admin login
│   │   ├── admin.html        ← Admin dashboard (sidebar + tables)
│   │   └── scheme_form.html  ← Add / Edit scheme form
│   └── static/
│       ├── css/style.css     ← Modern dark SaaS stylesheet (glassmorphism, gradients)
│       └── js/script.js      ← Interactivity, animations & form validation
│
├── database/
│   └── schema.sql      ← Tables + sample data
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### Step 1 – Prerequisites
- Python 3.10+
- MySQL Server 8.0+
- pip

---

### Step 2 – Configure MySQL credentials

Open `backend/database.py` and update your MySQL credentials:

```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "YOUR_PASSWORD_HERE",   # ← change this
    "database": "schemo_db",
}
```

---

### Step 3 – Create the database and tables

Log into MySQL and run the schema file:

```bash
# In your terminal / MySQL shell:
mysql -u root -p < database/schema.sql
```

Or open MySQL Workbench / phpMyAdmin and execute the contents of `database/schema.sql`.

This will:
- Create the `schemo_db` database
- Create the `users`, `admins`, and `schemes` tables
- Insert **12 sample government schemes**

---

### Step 4 – Install Python dependencies

```bash
# From the project root folder
pip install -r requirements.txt
```

---

### Step 5 – Run the Flask application

```bash
cd backend
python app.py
```

You should see:

```
[Schemo] Default admin created  →  username: admin | password: admin123
 * Running on http://0.0.0.0:5000
```

Open your browser at **http://127.0.0.1:5000**

---

## 🔐 Default Admin Credentials

| Username | Password |
|----------|----------|
| `admin`  | `admin123` |

> Admin login is at: **http://127.0.0.1:5000/admin/login**

---

## 🌐 Application Routes

| Route                          | Description                      |
|-------------------------------|----------------------------------|
| `/`                           | Landing page                     |
| `/signup`                     | User registration                |
| `/login`                      | User login                       |
| `/logout`                     | Logout                           |
| `/dashboard`                  | User dashboard (login required)  |
| `/schemes`                    | Browse all schemes (public)      |
| `/admin/login`                | Admin login                      |
| `/admin/dashboard`            | Admin dashboard (CRUD)           |
| `/admin/scheme/add`           | Add new scheme                   |
| `/admin/scheme/edit/<id>`     | Edit a scheme                    |
| `/admin/scheme/delete/<id>`   | Delete a scheme                  |
| `/admin/user/delete/<id>`     | Delete a user                    |

---

## 🗄️ Database Schema (Key Tables)

### `users`
| Column | Type | Notes |
|---|---|---|
| `id` | INT, PK | Auto increment |
| `name` | VARCHAR | Full name |
| `email` | VARCHAR | Unique login identifier |
| `phone_number` | VARCHAR(10) | Unique, 10 digits |
| `password` | VARCHAR | Hashed with Werkzeug PBKDF2 |
| `age` | INT | Used for scheme eligibility |
| `gender` | VARCHAR | Male / Female / Other |
| `community` | VARCHAR | General, OBC, SC, ST, etc. |
| `occupation` | VARCHAR | Student, Farmer, etc. |
| `state` | VARCHAR | Indian state or UT |
| `created_at` | DATETIME | Registration timestamp |

### `schemes`
| Column | Type | Notes |
|---|---|---|
| `id` | INT, PK | Auto increment |
| `scheme_name` | VARCHAR | Scheme title |
| `description` | TEXT | Short description |
| `community` | VARCHAR | Target community (or "All") |
| `min_age` / `max_age` | INT | Eligibility age range |
| `max_income` | BIGINT | Max annual income (0 = no limit) |
| `benefits` | TEXT | What the scheme offers |
| `eligibility` | TEXT | Eligibility conditions |
| `documents_required` | TEXT | Required documents list |
| `deadline` | DATE | Application deadline (nullable) |
| `official_link` | VARCHAR | Official govt portal URL |

---

## 🎯 Eligibility Logic

When a logged-in user visits their dashboard, the app queries schemes where:
1. The **community** field matches the user's community OR is set to `All`
2. The user's **age** falls within the scheme's `min_age`–`max_age` range

Deadline logic is applied after fetching:
- If `deadline < today` → scheme is marked **Expired** (Apply button disabled)
- If `deadline >= today` → scheme is **Active**
- If no deadline → scheme is **Ongoing**

---

## 🎨 UI/UX Design System (v2 – 18 Mar 2026)

The UI was fully redesigned to a modern dark SaaS aesthetic with:

- **Theme:** Deep dark background (`#0A0A0A`) with blue (`#3B82F6`) and purple (`#8B5CF6`) gradient accents
- **Glassmorphism:** Semi-transparent cards with `backdrop-filter: blur(16px)` throughout
- **Icons:** [Lucide Icons](https://lucide.dev) loaded via CDN
- **Typography:** Inter (Google Fonts) — 300 to 900 weight range
- **Animations:** Intersection Observer staggered fade-in for cards and sections
- **Toasts:** Auto-dismiss flash notifications replacing plain flash banners
- **Components updated:**
  - Sticky glassmorphic navbar with Lucide brand icon
  - Hero section with gradient heading and animated CTA
  - Feature & step cards with hover lift effect
  - Auth pages with split-screen layout (form + info panel)
  - Dashboard with stat cards and profile banner
  - Scheme cards with status badges (Active / Expired / Ongoing)
  - Admin panel with sticky sidebar and modern data tables

---

## 🛡️ Security

- Passwords are hashed using **Werkzeug PBKDF2-SHA256** (never stored as plain text)
- Sessions are server-side with `HttpOnly` cookies
- All admin routes are protected by an `@admin_required` decorator
- All user routes are protected by a `@login_required` decorator
- Phone number validated to exactly 10 digits (frontend + backend)

---

## 🖥️ Tech Stack

| Layer      | Technology                                  |
|------------|---------------------------------------------|
| Backend    | Python 3.10+, Flask 3.x                     |
| Database   | MySQL 8, mysql-connector-python             |
| Frontend   | HTML5, Vanilla CSS3, JavaScript (ES6+)      |
| Icons      | Lucide Icons (CDN)                          |
| Fonts      | Google Fonts — Inter                        |
| Auth       | Werkzeug PBKDF2-SHA256 + Flask sessions     |

---

## 📋 Changelog

### v2.1 – 18 March 2026 (UI/UX Polish Pass)
- ✅ Navbar brand redesigned — gradient icon box (blue→purple square) replacing plain icon
- ✅ Removed stray separator dot from navbar center
- ✅ Admin nav link now shows Shield icon when logged in as admin
- ✅ Hero section — added subtle mesh grid overlay (60×60px) that fades at edges for premium tech feel
- ✅ Hero background upgraded to 3-layer elliptical gradient radial glows (deeper depth)
- ✅ Hero stat numbers (12+, 8, 28+) now use blue→purple gradient text
- ✅ Toast notifications now prefixed with contextual Lucide icons (✅ success, ⚠️ warning, ℹ️ info, ❌ error)
- ✅ Footer links updated with Lucide icons per link
- ✅ Schemes page hero centred with proper padding and constrained subtitle width
- ✅ `base.html` cleaned up and footer grid improved

### v2.0 – 18 March 2026
- ✅ Complete UI/UX overhaul to modern dark SaaS design
- ✅ Added Lucide Icons across all templates
- ✅ Redesigned `signup.html` — professional split layout with sticky info panel
- ✅ Redesigned `login.html` — split layout with benefit panel
- ✅ Redesigned `dashboard.html` — stat cards with icons, glassmorphic scheme cards
- ✅ Redesigned `schemes.html` — glass cards, integrated filter bar, removed debug banner
- ✅ Added phone number field to user registration (10-digit validation)
- ✅ Added scheme deadline logic (Active / Expired / Ongoing status)
- ✅ Fixed ₹ (Rupee) symbol encoding corruption in database
- ✅ Added staggered fade-in scroll animations
- ✅ Added auto-dismiss toast notifications
- ✅ Removed "Annual Income" field from signup (not in DB schema)
- ✅ Updated `style.css` with full glassmorphism design system

### v1.0 – March 2026
- ✅ Initial project setup (Flask + MySQL)
- ✅ User authentication (signup, login, logout)
- ✅ Scheme eligibility matching
- ✅ Admin panel (CRUD for schemes and users)
- ✅ 12 sample government schemes seeded

---

*Built with ❤️ for Indian citizens — Schemo*
