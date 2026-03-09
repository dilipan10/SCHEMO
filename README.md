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
│   │   ├── base.html         ← Shared layout (navbar, footer)
│   │   ├── index.html        ← Landing page
│   │   ├── signup.html       ← User registration
│   │   ├── login.html        ← User login
│   │   ├── dashboard.html    ← User dashboard + eligible schemes
│   │   ├── schemes.html      ← Public schemes listing
│   │   ├── admin_login.html  ← Admin login
│   │   ├── admin.html        ← Admin dashboard
│   │   └── scheme_form.html  ← Add / Edit scheme form
│   └── static/
│       ├── css/style.css     ← Premium dark UI stylesheet
│       └── js/script.js      ← Interactivity & validation
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

## 🎯 Eligibility Logic

When a logged-in user visits their dashboard, the app queries schemes where:
1. The **community** field matches the user's community OR is set to `All`
2. The user's **age** falls within the scheme's `min_age`–`max_age` range
3. The user's **annual income** is ≤ the scheme's `max_income` (0 = no limit)

---

## 🛡️ Security

- Passwords are hashed using **Werkzeug PBKDF2-SHA256** (never stored as plain text)
- Sessions are server-side with `HttpOnly` cookies
- All admin routes are protected by an `@admin_required` decorator
- All user routes are protected by a `@login_required` decorator

---

## 🖥️ Tech Stack

| Layer      | Technology              |
|------------|------------------------|
| Backend    | Python, Flask 3.x      |
| Database   | MySQL 8, mysql-connector-python |
| Frontend   | HTML5, CSS3, JavaScript (Vanilla) |
| Auth       | Werkzeug password hashing + Flask sessions |

---

*Built with ❤️ for Indian citizens — Schemo*
