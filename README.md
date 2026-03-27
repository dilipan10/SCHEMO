# Schemo – Government Scheme Aggregator Portal

> A full-stack Flask + Supabase web app where Indian citizens can register, log in, and discover government welfare schemes they are eligible for — with AI-powered matching, voice input, real-time scraping, and SMS alerts.

---

## 📁 Project Structure

```
schemo/
├── backend/
│   ├── app.py          ← Flask entry point
│   ├── routes.py       ← All URL routes (Blueprint)
│   ├── models.py       ← Supabase query functions
│   ├── database.py     ← Supabase client setup
│   ├── sms.py          ← MSG91 OTP + Scheme SMS alerts
│   └── scraper.py      ← Web scraper (MyScheme.gov.in, India.gov.in)
│
├── frontend/
│   ├── templates/
│   │   ├── base.html           ← Shared layout (navbar, footer, chatbot widget)
│   │   ├── index.html          ← Landing page
│   │   ├── signup.html         ← User registration (+ Google OAuth)
│   │   ├── login.html          ← User login (+ Google OAuth)
│   │   ├── sso_callback.html   ← Clerk Google OAuth callback handler
│   │   ├── dashboard.html      ← User dashboard (AI scores, tracker, dark mode)
│   │   ├── schemes.html        ← Public schemes listing with filters
│   │   ├── admin_login.html    ← Admin login
│   │   ├── admin.html          ← Admin dashboard (CRUD + analytics)
│   │   ├── scheme_form.html    ← Add / Edit scheme form
│   │   ├── upload_csv.html     ← Bulk CSV scheme import
│   │   └── scrape.html         ← Live scrape from govt websites
│   └── static/
│       ├── css/style.css       ← Dark SaaS stylesheet (glassmorphism)
│       └── js/script.js        ← Interactivity and animations
│
├── database/
│   └── schema.sql      ← Reference schema (actual DB is Supabase)
│
├── render.yaml         ← Render.com deployment config
├── Procfile            ← Gunicorn start command
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### Prerequisites
- Python 3.10+
- Supabase account (free tier works)

### Step 1 — Clone and install

```bash
pip install -r requirements.txt
```

### Step 2 — Configure `.env`

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_key
FLASK_SECRET_KEY=your-secret-key
GROQ_API_KEY=your_groq_api_key
CLERK_PUBLISHABLE_KEY=your_clerk_pk
MSG91_AUTH_KEY=your_msg91_key
MSG91_TEMPLATE_ID=your_dlt_template_id
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_password
```

### Step 3 — Run

```bash
python backend/app.py
```

Open **http://127.0.0.1:5000**

---

## 🔐 Admin Access

| Username | Password |
|----------|----------|
| Set in `.env` → `ADMIN_USERNAME` | `ADMIN_PASSWORD` |

Admin login: **http://127.0.0.1:5000/admin/login**

---

## 🌐 Routes

| Route | Description |
|---|---|
| `/` | Landing page |
| `/signup` | Register (email/password or Google) |
| `/login` | Login (email/password or Google) |
| `/sso-callback` | Clerk Google OAuth callback |
| `/logout` | Logout |
| `/dashboard` | User dashboard (login required) |
| `/schemes` | Browse all schemes (public) |
| `/admin/login` | Admin login |
| `/admin/dashboard` | Admin panel |
| `/admin/scheme/add` | Add scheme |
| `/admin/scheme/edit/<id>` | Edit scheme |
| `/admin/scheme/delete/<id>` | Delete scheme |
| `/admin/scheme/upload-csv` | Bulk CSV import |
| `/admin/scheme/sample-csv` | Download sample CSV |
| `/admin/scrape` | Scrape live govt websites |
| `/api/chatbot` | AI chatbot (POST) |
| `/api/eligibility-score` | Groq AI match score (POST) |
| `/api/schemes/chatbot-search` | Scheme search for chatbot (GET) |
| `/api/schemo/stats` | Admin analytics (GET) |

---

## ✅ Current Features

### Authentication
- Email + password login/signup (direct, no OTP step)
- Google OAuth via Clerk (login + signup)
- Session-based auth with `@login_required` / `@admin_required`
- Passwords hashed with Werkzeug PBKDF2-SHA256

### User Dashboard
- Eligible schemes matched by age, community, occupation
- **AI Eligibility Score** — Groq Llama 3.3 scores each scheme 0–100% with reason
- **Profile Completion Bar** — shows % of profile filled
- **Deadline Badge** — red pulsing badge when deadline ≤ 7 days
- **Application Tracker** — Saved / Applied / Documents Sent / Approved (localStorage)
- **Voice Read-Aloud** — 🔊 button reads scheme details using browser TTS
- **Search & Filter** — live search + status filter on dashboard
- **Dark / Light Mode** toggle (persists in localStorage)

### Schemes
- Public scheme listing with search, community filter, status filter
- Scheme detail modal with eligibility, benefits, documents, where-to-get-docs guide
- Google Maps links for nearest Esai Maiyam / CSC / District Collector

### AI Chatbot (SchemoBot)
- Powered by Groq Llama 3.3 with Supabase dataset as context
- Answers from your real scheme database first
- Built-in keyword fallback (no API key needed)
- **Voice input** — mic button for speech-to-text
- **Scheme search box** inside chatbot — search DB live, click to ask bot
- Tamil language support

### Admin Panel
- User management (view, delete)
- Scheme CRUD (add, edit, delete)
- **Bulk CSV upload** with sample CSV download
- **Live web scraping** — scrape MyScheme.gov.in + India.gov.in, auto-import new schemes
- Analytics dashboard (user stats, trends, charts)

### Notifications
- **SMS alerts** via MSG91 — sent to matching users when a new scheme is added
- **SMS OTP** via MSG91 for 2FA on login and signup

### Deployment
- Ready for **Render.com** (free tier)
- `render.yaml` + `Procfile` included
- Gunicorn production server

---

## 🗄️ Database (Supabase)

### `users`
| Column | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key |
| `name` | text | Full name |
| `email` | text | Unique |
| `phone_number` | text | 10-digit Indian number |
| `password` | text | Hashed (PBKDF2) |
| `age` | int | For eligibility matching |
| `gender` | text | Male / Female / Other |
| `community` | text | General, OBC, SC, ST, EWS, Minority |
| `occupation` | text | Student, Farmer, etc. |
| `state` | text | Indian state or UT |
| `created_at` | timestamptz | Auto |

### `schemes`
| Column | Type | Notes |
|---|---|---|
| `id` | int | Primary key |
| `scheme_name` | text | |
| `description` | text | |
| `eligibility` | text | |
| `community` | text | Comma-separated or "All" |
| `min_age` / `max_age` | int | Age range |
| `max_income` | float | 0 = no limit |
| `benefits` | text | |
| `documents_required` | text | |
| `deadline` | date | Nullable |
| `official_link` | text | |

### `admins`
| Column | Type |
|---|---|
| `id` | int |
| `username` | text |
| `password` | text (hashed) |

---

## 🖥️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask 3.x, Gunicorn |
| Database | Supabase (PostgreSQL) |
| AI | Groq API — Llama 3.3 70B |
| Auth | Clerk (Google OAuth) + Flask sessions |
| SMS | MSG91 |
| Scraping | requests + BeautifulSoup4 |
| Frontend | HTML5, Vanilla CSS3, JavaScript ES6+ |
| Icons | Lucide Icons (CDN) |
| Fonts | Google Fonts — Inter |
| Deployment | Render.com |

---

## 📋 Changelog

### v3.0 — 27 March 2026
- ✅ Migrated database from MySQL → **Supabase** (PostgreSQL)
- ✅ Added **Google OAuth** via Clerk (login + signup)
- ✅ Added **Groq AI eligibility score** per scheme card (Llama 3.3)
- ✅ Added **AI chatbot** powered by Groq with live Supabase dataset context
- ✅ Added **voice input** (mic button) in chatbot
- ✅ Added **scheme search** inside chatbot widget
- ✅ Added **web scraper** (MyScheme.gov.in + India.gov.in)
- ✅ Added **bulk CSV upload** for schemes
- ✅ Added **SMS alerts** via MSG91 on new scheme added
- ✅ Added **application tracker** (Saved/Applied/Documents Sent/Approved)
- ✅ Added **profile completion bar**
- ✅ Added **deadline badge** (red pulse when ≤ 7 days)
- ✅ Added **dark/light mode** toggle
- ✅ Added **voice read-aloud** on scheme cards
- ✅ Added **admin analytics** with charts
- ✅ Removed OTP step from login/signup (direct email+password)
- ✅ Removed MySQL dependency entirely
- ✅ Deployment config for Render.com

### v2.2 — 19 March 2026
- ✅ Admin dashboard overhaul with glassmorphism sidebar
- ✅ Real-time analytics engine with trend calculations
- ✅ Unique phone number validation on signup

### v2.0 — 18 March 2026
- ✅ Complete UI/UX overhaul to dark SaaS design
- ✅ Lucide Icons, glassmorphism, Inter font
- ✅ Split-screen auth pages
- ✅ Scheme deadline logic (Active/Expired/Ongoing)

### v1.0 — March 2026
- ✅ Initial Flask + MySQL setup
- ✅ User auth, scheme eligibility matching, admin CRUD

---

*Built with ❤️ for Indian citizens — Schemo v3.0*
