"""
routes.py  -  All Flask URL routes for Schemo
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, jsonify
)
from functools import wraps
from datetime import date
import models
from sms import send_otp_sms

bp = Blueprint("main", __name__)


# =============================================================================
# BUILT-IN SMART CHATBOT  (works with NO API key — always available)
# =============================================================================

SCHEME_KB = {
    "greeting": {
        "keywords": ["hi","hello","hey","help","start","namaste","vanakkam","helo",
                     "good morning","good evening","greet"],
        "reply": (
            "👋 **Vanakkam! Welcome to SchemoBot!**\n\n"
            "I'm your AI guide for **Indian Government Schemes**. I can help you find:\n\n"
            "🎓 Student Scholarships\n"
            "🌾 Farmer & Agriculture Schemes\n"
            "👩 Women & Girl Child Welfare\n"
            "💼 Employment & Business Schemes\n"
            "🏠 Housing Schemes\n"
            "🏥 Health & Medical Schemes\n"
            "👴 Senior Citizen Benefits\n"
            "🤝 SC / ST / OBC Welfare\n\n"
            "**Just tell me who you are** and I'll guide you! 😊"
        )
    },
    "student": {
        "keywords": ["student","scholarship","study","education","college","school",
                     "university","degree","10th","12th","nsp","vidya",
                     "படிப்பு","மாணவர்","உதவித்தொகை","கல்வி","கல்லூரி"],
        "reply": (
            "🎓 **Schemes for Students & Education**\n\n"
            "**1. National Scholarship Portal (NSP)**\n"
            "• Eligibility: Students from Class 1 to PG level\n"
            "• Benefits: ₹500 – ₹20,000/year scholarship\n"
            "• Documents: Aadhaar, income certificate, marksheet, bank passbook\n"
            "• Deadline: Usually October–November every year\n"
            "• 🔗 scholarships.gov.in\n\n"
            "**2. PM Vidya Lakshmi (Education Loan)**\n"
            "• Eligibility: Students admitted to recognised institutions\n"
            "• Benefits: Education loan up to ₹6.5 lakh (no collateral)\n"
            "• Documents: Admission letter, Aadhaar, income proof\n"
            "• 🔗 vidyalakshmi.co.in\n\n"
            "**3. Post-Matric Scholarship (SC/ST/OBC)**\n"
            "• Eligibility: SC/ST/OBC students in Class 11 and above\n"
            "• Benefits: Full tuition + maintenance allowance\n"
            "• Documents: Caste certificate, income certificate, Aadhaar\n"
            "• 🔗 scholarships.gov.in\n\n"
            "**4. Central Sector Scholarship**\n"
            "• Eligibility: Top 20 percentile in Class 12 board\n"
            "• Benefits: ₹10,000–₹20,000/year\n\n"
            "💡 Need info on a specific scholarship? Just ask!"
        )
    },
    "farmer": {
        "keywords": ["farmer","agriculture","farm","crop","kisan","farming","seed",
                     "irrigation","soil","cattle","dairy","animal",
                     "விவசாயி","விவசாயம்","நிலம்","பயிர்","கிசான்","கால்நடை"],
        "reply": (
            "🌾 **Schemes for Farmers & Agriculture**\n\n"
            "**1. PM Kisan Samman Nidhi**\n"
            "• Eligibility: All small & marginal farmers with cultivable land\n"
            "• Benefits: ₹6,000/year (₹2,000 in 3 installments directly to bank)\n"
            "• Documents: Aadhaar, land records, bank account\n"
            "• 🔗 pmkisan.gov.in\n\n"
            "**2. PM Fasal Bima Yojana (Crop Insurance)**\n"
            "• Eligibility: All farmers growing notified crops\n"
            "• Benefits: Full insurance coverage for crop loss due to natural calamity\n"
            "• Premium: 2% for Kharif, 1.5% for Rabi crops\n"
            "• Documents: Land record, bank account, Aadhaar\n"
            "• 🔗 pmfby.gov.in\n\n"
            "**3. Kisan Credit Card (KCC)**\n"
            "• Eligibility: All farmers, fishermen, self-help groups\n"
            "• Benefits: Credit up to ₹3 lakh at just 4% interest\n"
            "• Documents: Land records, Aadhaar, passport photo\n\n"
            "**4. PM Kisan Maan Dhan Yojana (Farmer Pension)**\n"
            "• Eligibility: Farmers aged 18–40 years\n"
            "• Benefits: ₹3,000/month pension after age 60\n\n"
            "**5. PM Krishi Sinchai Yojana**\n"
            "• Benefits: Irrigation support — 'Har Khet Ko Pani'\n"
            "• 🔗 pmksy.gov.in\n\n"
            "💡 Ask me about any specific farming scheme!"
        )
    },
    "women": {
        "keywords": ["women","woman","female","girl","mahila","widow","beti","mother",
                     "pregnant","maternity","self help group","shg",
                     "பெண்","மகளிர்","விதவை","பெண்கள்","அம்மா","கர்ப்பிணி"],
        "reply": (
            "👩 **Schemes for Women & Girl Child**\n\n"
            "**1. Beti Bachao Beti Padhao**\n"
            "• Eligibility: Girl children (0–18 years)\n"
            "• Benefits: Education & welfare support for girls\n"
            "• 🔗 wcd.nic.in\n\n"
            "**2. PM Ujjwala Yojana**\n"
            "• Eligibility: BPL women above 18 years\n"
            "• Benefits: Free LPG gas connection + first refill free\n"
            "• Documents: Aadhaar, BPL ration card, bank account\n"
            "• 🔗 pmujjwalayojana.com\n\n"
            "**3. Sukanya Samriddhi Yojana**\n"
            "• Eligibility: Parents of girl child below 10 years\n"
            "• Benefits: 8.2% p.a. savings for girl's education/marriage\n"
            "• Open at any post office or authorised bank\n\n"
            "**4. PM Matru Vandana Yojana**\n"
            "• Eligibility: Pregnant & lactating mothers (first live birth)\n"
            "• Benefits: ₹5,000 cash benefit in 3 installments\n"
            "• Documents: Aadhaar, bank account, MCP card\n\n"
            "**5. Mahila Shakti Kendra**\n"
            "• Skill development & employment support for rural women\n\n"
            "💡 Tell me your state for more women welfare schemes!"
        )
    },
    "job": {
        "keywords": ["job","employment","work","unemployed","rozgar","career","business",
                     "skill","training","apprentice","mudra","startup","vendor","loan",
                     "வேலை","தொழில்","வேலையில்லாமை","கடன்","சுயதொழில்"],
        "reply": (
            "💼 **Schemes for Employment & Business**\n\n"
            "**1. MGNREGS (100 Days Employment Guarantee)**\n"
            "• Eligibility: Any rural adult willing to do unskilled work\n"
            "• Benefits: 100 days guaranteed employment per year\n"
            "• Wage: ₹220–₹350/day (state-wise)\n"
            "• Documents: Aadhaar, job card (from Gram Panchayat)\n\n"
            "**2. PM Mudra Yojana (Business Loan)**\n"
            "• Eligibility: Small business owners, entrepreneurs\n"
            "• Benefits: Loans up to ₹10 lakh — NO collateral needed!\n"
            "  - Shishu: up to ₹50,000\n"
            "  - Kishore: ₹50,000 – ₹5 lakh\n"
            "  - Tarun: ₹5 lakh – ₹10 lakh\n"
            "• 🔗 mudra.org.in\n\n"
            "**3. PM Kaushal Vikas Yojana (Skill Training)**\n"
            "• Free skill training + ₹8,000 reward on certification\n"
            "• 🔗 pmkvyofficial.org\n\n"
            "**4. Startup India**\n"
            "• Eligibility: DPIIT-recognised startups\n"
            "• Benefits: Tax exemption, funding support, mentorship\n"
            "• 🔗 startupindia.gov.in\n\n"
            "**5. PM SVANidhi (Street Vendor Loan)**\n"
            "• Benefits: Working capital loan ₹10,000–₹50,000\n\n"
            "💡 Tell me your occupation for tailored suggestions!"
        )
    },
    "housing": {
        "keywords": ["house","home","housing","shelter","awas","flat","plot","room",
                     "construction","build","bpl","ration",
                     "வீடு","குடியிருப்பு","இல்லம்","கட்டுமானம்","குடிசை"],
        "reply": (
            "🏠 **Schemes for Housing**\n\n"
            "**1. PM Awas Yojana – Gramin (Rural)**\n"
            "• Eligibility: BPL families in rural areas without a pucca house\n"
            "• Benefits: ₹1.20 lakh (plain) / ₹1.30 lakh (hilly/NE states)\n"
            "• Documents: Aadhaar, BPL card, bank account\n"
            "• Apply: Through Gram Panchayat / Block Office\n"
            "• 🔗 pmayg.nic.in\n\n"
            "**2. PM Awas Yojana – Urban (City)**\n"
            "• Eligibility: EWS/LIG/MIG families in cities without pucca house\n"
            "• Benefits: Home loan interest subsidy up to ₹2.67 lakh\n"
            "• 🔗 pmaymis.gov.in\n\n"
            "**3. Indira Awas Yojana (IAY)**\n"
            "• Free housing units for poorest families\n"
            "• Apply via local CSC centre or Panchayat\n\n"
            "**4. Credit Linked Subsidy Scheme (CLSS)**\n"
            "• Home loan subsidy for middle income families\n"
            "• Subsidy up to ₹2.35 lakh on home loan interest\n\n"
            "💡 Tell me your state for specific state housing schemes!"
        )
    },
    "health": {
        "keywords": ["health","medical","hospital","treatment","insurance","ayushman",
                     "medicine","doctor","surgeon","disease","illness",
                     "உடல்நலம்","மருத்துவம்","ஆரோக்கியம்","மருத்துவமனை","நோய்"],
        "reply": (
            "🏥 **Schemes for Health & Medical**\n\n"
            "**1. Ayushman Bharat – PM Jan Arogya Yojana (PMJAY)**\n"
            "• Eligibility: Poor & vulnerable families (SECC database listed)\n"
            "• Benefits: Health insurance up to ₹5 lakh/year per family!\n"
            "• Cashless treatment at 25,000+ empanelled hospitals\n"
            "• Check eligibility: mera.pmjay.gov.in\n\n"
            "**2. Janani Suraksha Yojana (JSY)**\n"
            "• Eligibility: Pregnant women from BPL families\n"
            "• Benefits: Cash incentive for institutional delivery\n"
            "  - Rural: ₹1,400 | Urban: ₹1,000\n\n"
            "**3. National Health Mission (NHM)**\n"
            "• Free medicines & diagnostics at government hospitals\n"
            "• Free ambulance service (108) across India\n\n"
            "**4. PM Surakshit Matritva Abhiyan**\n"
            "• Free antenatal checkups on 9th of every month\n\n"
            "**5. Rashtriya Arogya Nidhi**\n"
            "• Financial help for BPL patients with life-threatening diseases\n\n"
            "💡 Need info on a specific disease or medical support?"
        )
    },
    "senior": {
        "keywords": ["senior","old","elderly","pension","aged","retire","60","70","80",
                     "grandfather","grandmother","old age",
                     "முதியோர்","வயதான","ஓய்வூதியம்","பெரியவர்","நலன்"],
        "reply": (
            "👴 **Schemes for Senior Citizens**\n\n"
            "**1. Indira Gandhi National Old Age Pension (IGNOAP)**\n"
            "• Eligibility: BPL citizens above 60 years\n"
            "• Benefits: ₹200–₹500/month pension\n"
            "• Documents: Aadhaar, age proof, BPL certificate\n"
            "• Apply through Gram Panchayat / Ward Office\n\n"
            "**2. Atal Pension Yojana**\n"
            "• Eligibility: 18–40 years (plan now for your future!)\n"
            "• Benefits: Guaranteed pension ₹1,000–₹5,000/month after age 60\n"
            "• Enrol at any bank branch or post office\n\n"
            "**3. Senior Citizen Savings Scheme (SCSS)**\n"
            "• Eligibility: 60+ years\n"
            "• Benefits: 8.2% interest per year (quarterly payout)\n"
            "• Maximum deposit: ₹30 lakh\n"
            "• Available at post offices & banks\n\n"
            "**4. PM Vaya Vandana Yojana (PMVVY)**\n"
            "• Pension scheme for senior citizens via LIC\n"
            "• Guaranteed 7.4% return on investment\n\n"
            "**5. Rashtriya Vayoshri Yojana**\n"
            "• Free assistive devices (spectacles, hearing aids, wheelchairs)\n"
            "• For BPL senior citizens above 60\n\n"
            "💡 Ask about any specific senior citizen benefit!"
        )
    },
    "sc_st": {
        "keywords": ["sc","st","obc","dalit","scheduled caste","scheduled tribe","backward",
                     "tribal","adivasi","minority","ebc","minority",
                     "அட்டவணை சாதி","பழங்குடி","பிற்படுத்தப்பட்ட","ஆதிவாசி"],
        "reply": (
            "🤝 **Schemes for SC / ST / OBC Communities**\n\n"
            "**1. Post-Matric Scholarship**\n"
            "• Eligibility: SC/ST/OBC students in Class 11 and above\n"
            "• Benefits: Full tuition + maintenance allowance\n"
            "• 🔗 scholarships.gov.in\n\n"
            "**2. Dr. Ambedkar Post-Matric Scholarship (OBC/EBC)**\n"
            "• For OBC & EBC students in higher education\n"
            "• Income limit: ₹2.5 lakh per year\n\n"
            "**3. Standup India**\n"
            "• Eligibility: SC/ST/Women entrepreneurs\n"
            "• Benefits: Loans ₹10 lakh – ₹1 crore for new business\n"
            "• 🔗 standupmitra.in\n\n"
            "**4. National SC/ST Hub**\n"
            "• Support for SC/ST entrepreneurs in government tenders\n"
            "• 🔗 nscshub.udyamimitra.in\n\n"
            "**5. Free Coaching Scheme**\n"
            "• Free coaching for UPSC, SSC, banking exams\n"
            "• For SC/ST students through NSFDC\n\n"
            "**6. Van Dhan Vikas Yojana (Tribal)**\n"
            "• Benefits: Tribal entrepreneurship & livelihood support\n\n"
            "💡 Tell me your community & state for more!"
        )
    },
    "tamil": {
        "keywords": ["என்ன","திட்டம்","உதவி","வணக்கம்","யாருக்கு","எனக்கு","நான்",
                     "தமிழ்","தேவை","கேள்வி","மாணவர்","விவசாயி","பெண்","வேலை",
                     "tamil", "language", "lang", "speak in tamil", "talk in tamil"],
        "reply": (
            "**ஆம், தாராளமாக தமிழில் பேசலாம்!** 🙏\n\n"
            "வணக்கம்! நான் SchemoBot — உங்களுக்கு உதவி செய்ய தயாராக இருக்கிறேன்.\n\n"
            "இந்திய அரசு திட்டங்களைப் பற்றி நான் உங்களுக்கு தெளிவாக விளக்குவேன்.\n"
            "நீங்கள் எந்த வகையான திட்டங்களை தேடுகிறீர்கள்?\n\n"
            "👇 உங்கள் தேவையை கீழே தெரிவிக்கவும்:\n"
            "• 🎓 **மாணவர் உதவித்தொகை**\n"
            "• 🌾 **விவசாயி திட்டங்கள்**\n"
            "• 👩 **பெண்கள் நலத்திட்டங்கள்**\n"
            "• 💼 **வேலைவாய்ப்பு மற்றும் கடன்**\n"
            "• 🏠 **வீட்டு திட்டங்கள்**\n"
            "• 🏥 **சுகாதார திட்டங்கள்**\n\n"
            "தமிழிலிலேயே கேளுங்கள் — நான் பதில் சொல்கிறேன்! 😊"
        )
    },
}

DEFAULT_REPLY = (
    "I'm here to help you find **Indian Government Schemes**! 🇮🇳\n\n"
    "Please tell me about yourself:\n"
    "• Are you a **student**, **farmer**, **job seeker**, or **entrepreneur**?\n"
    "• Looking for **health**, **housing**, or **women welfare** schemes?\n"
    "• From **SC/ST/OBC** community? Or a **senior citizen**?\n\n"
    "The more you share, the better I can guide you! 😊\n\n"
    "_You can also check: [india.gov.in](https://india.gov.in)_"
)


def smart_reply(user_message: str) -> str:
    """Rule-based smart scheme matcher — no API key needed."""
    msg = user_message.lower().strip()
    best_cat, best_score = None, 0
    for cat, data in SCHEME_KB.items():
        score = sum(1 for kw in data["keywords"] if kw in msg)
        if score > best_score:
            best_score, best_cat = score, cat
    if best_score > 0:
        return SCHEME_KB[best_cat]["reply"]
    return DEFAULT_REPLY


# =============================================================================
# CHATBOT API ROUTE — Hybrid: Groq first, smart built-in fallback
# =============================================================================

SYSTEM_PROMPT = (
    "You are Schemo AI — a world-class, professional AI Advisor specialized in Indian Government Schemes. "
    "Your personality: Empathetic, expert, accurate, and extremely helpful. "
    "Schemo is a portal for Indian citizens (Students, Farmers, Women, Entrepreneurs, etc.) to discover benefits. "
    "RULES: "
    "1. If the user asks in Tamil, reply in Tamil. If English, reply in English. "
    "2. For every scheme provide: Name, Eligibility, Benefits, Steps to Apply, and official Link. "
    "3. Use Markdown formatting: bold headers, bullet points. "
    "4. Be conversational but concise. Use professional emojis. "
    "5. Help the user navigate their life goals using government resources."
)


@bp.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json(force=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message!"}), 200

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if api_key:
        try:
            from groq import Groq

            history = data.get("history", [])
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            for turn in history:
                role = turn.get("role", "user")
                # Groq uses 'assistant' not 'model'
                if role == "model":
                    role = "assistant"
                content = turn.get("content") or (
                    turn.get("parts", [""])[0]
                    if isinstance(turn.get("parts"), list)
                    else turn.get("parts", "")
                )
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": str(content)})

            messages.append({"role": "user", "content": user_message})

            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.8,
                max_tokens=1024,
            )
            return jsonify({"reply": response.choices[0].message.content}), 200

        except Exception as e:
            print(f"[Bot Debug] Groq failed: {e}")

    # Built-in fallback if Groq fails
    return jsonify({"reply": smart_reply(user_message)}), 200


# =============================================================================
# DECORATORS
# =============================================================================

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


# =============================================================================
# PUBLIC ROUTES
# =============================================================================

@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/sso-callback")
def sso_callback():
    """Clerk SSO callback — Clerk JS handles the token, then syncs with backend."""
    return render_template("sso_callback.html")


@bp.route("/schemes")
def schemes():
    all_schemes = models.get_all_schemes()
    current_date = date.today()
    for s in all_schemes:
        dl = s.get("deadline")
        if dl:
            if isinstance(dl, str):
                from datetime import datetime
                try:
                    dl = datetime.strptime(dl, "%Y-%m-%d").date()
                    s["deadline"] = dl
                except Exception:
                    pass
            s["status"] = "Expired" if isinstance(dl, date) and dl < current_date else "Active"
        else:
            s["status"] = "Active"
    return render_template("schemes.html", schemes=all_schemes)


@bp.route("/api/schemes/search")
def api_search_schemes():
    """JSON search endpoint for live scheme search."""
    q = request.args.get("q", "").strip().lower()
    community = request.args.get("community", "").strip()
    all_schemes = models.get_all_schemes()
    current_date = date.today()
    results = []
    for s in all_schemes:
        dl = s.get("deadline")
        if dl:
            if isinstance(dl, str):
                from datetime import datetime
                try:
                    dl = datetime.strptime(dl, "%Y-%m-%d").date()
                except Exception:
                    dl = None
            s["status"] = "Expired" if dl and dl < current_date else "Active"
            s["deadline_str"] = dl.strftime("%d %b %Y") if dl else ""
        else:
            s["status"] = "Active"
            s["deadline_str"] = ""
        # filter
        text_match = not q or q in s.get("scheme_name","").lower() or q in s.get("description","").lower() or q in s.get("eligibility","").lower()
        comm_match = not community or community.lower() in s.get("community","").lower()
        if text_match and comm_match:
            results.append(s)
    return jsonify(results)


# =============================================================================
# AUTH ROUTES
# =============================================================================

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        # Check if this is OTP verification step
        if request.form.get("otp_step") == "verify":
            stored_otp = session.get("signup_otp")
            stored_data = session.get("signup_data")
            user_otp = request.form.get("otp", "").strip()
            
            if not stored_otp or not stored_data:
                flash("Session expired. Please start again.", "danger")
                return redirect(url_for("main.signup"))
            
            if user_otp == stored_otp:
                # OTP verified — create user
                try:
                    user_id = models.create_user(
                        stored_data["name"], stored_data["email"], 
                        stored_data["phone_number"], stored_data["password"],
                        int(stored_data["age"]), stored_data["gender"],
                        stored_data["community"], stored_data["occupation"], 
                        stored_data["state"]
                    )
                    session.pop("signup_otp", None)
                    session.pop("signup_data", None)
                    flash("Account created successfully! Please log in.", "success")
                    return redirect(url_for("main.login"))
                except Exception as e:
                    flash(f"Error creating account: {e}", "danger")
            else:
                flash("Invalid OTP. Please try again.", "danger")
                return render_template("signup_otp.html", phone=stored_data["phone_number"])
        
        # Initial signup — collect data and send OTP
        name         = request.form.get("name", "").strip()
        email        = request.form.get("email", "").strip().lower()
        phone_number = request.form.get("phone_number", "").strip()
        password     = request.form.get("password", "")
        age          = request.form.get("age", 0)
        gender       = request.form.get("gender", "")
        community    = request.form.get("community", "")
        occupation   = request.form.get("occupation", "").strip()
        state        = request.form.get("state", "").strip()

        if not phone_number.isdigit() or len(phone_number) != 10:
            flash("Phone number must be exactly 10 digits.", "danger")
            return render_template("signup.html")

        if not all([name, email, phone_number, password, age, gender, community, occupation, state]):
            flash("All fields are required.", "danger")
            return render_template("signup.html")

        if models.get_user_by_email(email):
            flash("An account with this email already exists. Please log in.", "warning")
            return render_template("signup.html")

        if models.get_user_by_phone(phone_number):
            flash("This phone number is already registered. Please use another or log in.", "warning")
            return render_template("signup.html")

        # Generate 6-digit OTP
        import random
        otp = str(random.randint(100000, 999999))
        
        # Store in session
        session["signup_otp"] = otp
        session["signup_data"] = {
            "name": name, "email": email, "phone_number": phone_number,
            "password": password, "age": age, "gender": gender,
            "community": community, "occupation": occupation, "state": state
        }
        
        # Send OTP via SMS
        sms_sent = send_otp_sms(phone_number, otp)
        
        if sms_sent:
            flash(f"OTP sent to {phone_number}. Please check your SMS.", "success")
        else:
            # Fallback: show OTP in flash (dev mode)
            flash(f"SMS service unavailable. Your OTP is: {otp}", "warning")
        
        return render_template("signup_otp.html", phone=phone_number)

    return render_template("signup.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        # Check if OTP verification step
        if request.form.get("otp_step") == "verify":
            stored_otp = session.get("login_otp")
            stored_user_id = session.get("login_user_id")
            user_otp = request.form.get("otp", "").strip()
            
            if not stored_otp or not stored_user_id:
                flash("Session expired. Please log in again.", "danger")
                return redirect(url_for("main.login"))
            
            if user_otp == stored_otp:
                user = models.get_user_by_id(stored_user_id)
                session.pop("login_otp", None)
                session.pop("login_user_id", None)
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                flash(f"Welcome back, {user['name']}!", "success")
                return redirect(url_for("main.dashboard"))
            else:
                flash("Invalid OTP. Please try again.", "danger")
                return render_template("login_otp.html")
        
        # Initial login — verify credentials
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = models.get_user_by_email(email)
        if user and models.verify_user_password(user, password):
            # Generate OTP for 2FA
            import random
            otp = str(random.randint(100000, 999999))
            session["login_otp"] = otp
            session["login_user_id"] = user["id"]
            
            # Send OTP via SMS
            phone = user.get("phone_number", "")
            sms_sent = send_otp_sms(phone, otp)
            
            if sms_sent:
                flash(f"OTP sent to your registered phone. Please check SMS.", "success")
            else:
                flash(f"SMS unavailable. Your OTP is: {otp}", "warning")
            
            return render_template("login_otp.html", phone=phone)
        else:
            flash("Invalid email or password. Please try again.", "danger")

    clerk_key = os.environ.get("CLERK_PUBLISHABLE_KEY", "")
    return render_template("login.html", clerk_publishable_key=clerk_key)


@bp.route("/api/auth/google", methods=["POST"])
def google_auth():
    """
    Handle Google Auth from frontend.
    Receives user info (name, email, pic) and syncs with local DB.
    """
    data  = request.get_json(force=True) or {}
    name  = data.get("name")
    email = data.get("email")

    if not email or not name:
        return jsonify({"error": "Missing profile info"}), 400

    try:
        user = models.get_or_create_google_user(name, email)
        if user:
            session["user_id"]   = user["id"]
            session["user_name"] = user["name"]
            # To show a nice welcome
            return jsonify({
                "success": True, 
                "redirect": url_for("main.dashboard"),
                "user_name": user["name"]
            }), 200
        else:
            return jsonify({"error": "Failed to create user"}), 500
    except Exception as e:
        print(f"[Auth Error] Google Login failed: {e}")
        return jsonify({"error": str(e)}), 500


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


# =============================================================================
# USER DASHBOARD
# =============================================================================

@bp.route("/dashboard")
@login_required
def dashboard():
    user = models.get_user_by_id(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("main.login"))

    eligible = models.get_eligible_schemes(user)
    current_date = date.today()
    for s in eligible:
        if s["deadline"] and s["deadline"] < current_date:
            s["status"] = "Expired"
        else:
            s["status"] = "Active"

    return render_template("dashboard.html", user=user, schemes=eligible)


# =============================================================================
# ADMIN AUTH
# =============================================================================

@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("is_admin"):
        return redirect(url_for("main.admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = models.get_admin_by_username(username)
        if admin and models.verify_admin_password(admin, password):
            session["is_admin"]       = True
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


# =============================================================================
# ADMIN DASHBOARD
# =============================================================================

@bp.route("/admin")
@bp.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    users   = models.get_all_users()
    schemes = models.get_all_schemes()
    current_date = date.today()
    for s in schemes:
        if s["deadline"] and s["deadline"] < current_date:
            s["status"] = "Expired"
        else:
            s["status"] = "Active"
    return render_template("admin.html", users=users, schemes=schemes)


@bp.route("/admin/user/delete/<int:user_id>", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    models.delete_user(user_id)
    flash("User deleted successfully.", "success")
    return redirect(url_for("main.admin_dashboard"))


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


@bp.route("/admin/scheme/delete/<int:scheme_id>", methods=["POST"])
@admin_required
def admin_delete_scheme(scheme_id):
    models.delete_scheme(scheme_id)
    flash("Scheme deleted successfully.", "success")
    return redirect(url_for("main.admin_dashboard"))


# =============================================================================
# ADMIN ANALYTICS API (Insights)
# =============================================================================

@bp.route("/api/schemo/stats")
@admin_required
def api_schemo_stats():
    """Returns all analytics data for the admin dashboard charts."""
    try:
        stats = models.get_user_stats()
        return jsonify(stats), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
