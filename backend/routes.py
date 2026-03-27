"""
routes.py  -  All Flask URL routes for Schemo
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, jsonify, current_app
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
    "tamilnadu": {
        "keywords": ["tamil nadu","tamilnadu","tn scheme","tamilnadu scheme","tamilnadu government",
                     "tn govt","state scheme","kalaignar","amma scheme","cm scheme",
                     "pudhumai penn","magalir urimai","innuyir kaapom","tn laptop",
                     "தமிழ்நாடு","தமிழ்நாடு திட்டம்","மாநில திட்டம்","முதலமைச்சர்","கலைஞர்"],
        "reply": (
            "🏛️ **Tamil Nadu Government Schemes**\n\n"
            "**1. Kalaignar Magalir Urimai Thittam**\n"
            "• Eligibility: Women above 21, head of family, income < ₹2.5 lakh/year\n"
            "• Benefits: ₹1,000/month direct cash transfer\n"
            "• Documents: Aadhaar, ration card, bank account\n"
            "• Apply: tn.gov.in or nearest Collectorate\n\n"
            "**2. Pudhumai Penn Scheme**\n"
            "• Eligibility: Girls who studied Class 6–12 in govt schools, now in higher education\n"
            "• Benefits: ₹1,000/month stipend until graduation\n"
            "• Documents: School TC, college admission proof, Aadhaar\n\n"
            "**3. CM's Breakfast Scheme**\n"
            "• Eligibility: Students in govt primary schools (Classes 1–5)\n"
            "• Benefits: Free nutritious breakfast every school day\n\n"
            "**4. Innuyir Kaapom (Health Insurance)**\n"
            "• Eligibility: TN residents with family income < ₹72,000/year\n"
            "• Benefits: Health coverage up to ₹5 lakh/year\n"
            "• Apply: Nearest govt hospital or CSC centre\n\n"
            "**5. TN Free Laptop Scheme**\n"
            "• Eligibility: Students entering Class 11 in govt schools\n"
            "• Benefits: Free laptop with internet connectivity\n\n"
            "**6. Kalaignar Kanavu Illam (Housing)**\n"
            "• Eligibility: BPL families in TN without pucca house\n"
            "• Benefits: Free house construction support\n"
            "• Apply: TNSCB / District Collectorate\n\n"
            "**7. Moovalur Ramamirtham Ammaiyar Scheme**\n"
            "• Eligibility: First-gen girls from govt schools joining higher education\n"
            "• Benefits: ₹1,000/month + ₹25,000 on graduation\n\n"
            "**8. TN Unorganised Workers Welfare Scheme**\n"
            "• Eligibility: Unorganised sector workers registered with TN Labour Dept\n"
            "• Benefits: Accident insurance, education aid, marriage assistance\n"
            "• Register: labour.tn.gov.in\n\n"
            "💡 Visit **tn.gov.in** for the complete list of state schemes!"
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
            "• 🏥 **சுகாதார திட்டங்கள்**\n"
            "• 🏛️ **தமிழ்நாடு திட்டங்கள்** — \"Tamil Nadu schemes\" என கேளுங்கள்!\n\n"
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
    "You are Schemo AI — a professional AI Advisor for Indian Government Schemes. "
    "You have access to a real database of schemes. When the user asks about schemes, "
    "use the SCHEME DATA provided in the context to give accurate answers. "
    "RULES: "
    "1. If the user asks in Tamil, reply in Tamil. If English, reply in English. "
    "2. Always refer to the scheme data provided — do not make up schemes. "
    "3. For every scheme provide: Name, Eligibility, Benefits, Documents, and official Link. "
    "4. Use Markdown formatting: bold headers, bullet points. "
    "5. Be conversational but concise. Use professional emojis."
)


def get_db_schemes_context(query: str) -> str:
    """Search Supabase schemes matching the query and return as context string."""
    try:
        all_schemes = models.get_all_schemes()
        q = query.lower()
        matched = []
        for s in all_schemes:
            text = f"{s.get('scheme_name','')} {s.get('description','')} {s.get('eligibility','')} {s.get('community','')}".lower()
            if any(word in text for word in q.split() if len(word) > 2):
                matched.append(s)
        # Top 5 matches
        matched = matched[:5]
        if not matched:
            return ""
        lines = ["**Schemes from our database:**\n"]
        for s in matched:
            lines.append(
                f"- **{s['scheme_name']}** | Community: {s.get('community','All')} | "
                f"Age: {s.get('min_age',0)}-{s.get('max_age',100)} | "
                f"Benefits: {s.get('benefits','')[:120]} | "
                f"Eligibility: {s.get('eligibility','')[:100]} | "
                f"Link: {s.get('official_link','')}"
            )
        return "\n".join(lines)
    except Exception as e:
        print(f"[DB Context Error] {e}")
        return ""


@bp.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json(force=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message!"}), 200

    # Always fetch relevant schemes from DB to ground the answer
    db_context = get_db_schemes_context(user_message)

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if api_key:
        try:
            from groq import Groq

            history = data.get("history", [])
            # Build system prompt with live DB context
            system_with_context = SYSTEM_PROMPT
            if db_context:
                system_with_context += f"\n\nCURRENT DATABASE CONTEXT:\n{db_context}"

            messages = [{"role": "system", "content": system_with_context}]

            for turn in history:
                role = turn.get("role", "user")
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
                temperature=0.7,
                max_tokens=1024,
            )
            return jsonify({"reply": response.choices[0].message.content}), 200

        except Exception as e:
            print(f"[Bot Debug] Groq failed: {e}")

    # Fallback: if DB has matches, show them; else use keyword KB
    if db_context:
        return jsonify({"reply": db_context + "\n\n💡 Ask me anything about these schemes!"}), 200
    return jsonify({"reply": smart_reply(user_message)}), 200


# =============================================================================
# SCHEME SEARCH API  (for chatbot search box)
# =============================================================================

@bp.route("/api/schemes/chatbot-search")
def chatbot_scheme_search():
    """Returns schemes matching a query — used by the chatbot search feature."""
    q = request.args.get("q", "").strip().lower()
    if not q or len(q) < 2:
        return jsonify([]), 200
    try:
        all_schemes = models.get_all_schemes()
        results = []
        for s in all_schemes:
            text = f"{s.get('scheme_name','')} {s.get('description','')} {s.get('eligibility','')} {s.get('community','')}".lower()
            if any(word in text for word in q.split() if len(word) > 2):
                results.append({
                    "id": s.get("id"),
                    "scheme_name": s.get("scheme_name"),
                    "description": s.get("description","")[:120],
                    "community": s.get("community"),
                    "benefits": s.get("benefits","")[:100],
                    "official_link": s.get("official_link",""),
                    "status": s.get("status","Active"),
                })
        return jsonify(results[:8]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    clerk_key = os.environ.get("CLERK_PUBLISHABLE_KEY", "")
    return render_template("sso_callback.html", clerk_publishable_key=clerk_key)


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

    clerk_key = os.environ.get("CLERK_PUBLISHABLE_KEY", "")

    if request.method == "POST":
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
            return render_template("signup.html", clerk_publishable_key=clerk_key)

        if not all([name, email, phone_number, password, age, gender, community, occupation, state]):
            flash("All fields are required.", "danger")
            return render_template("signup.html", clerk_publishable_key=clerk_key)

        if models.get_user_by_email(email):
            flash("An account with this email already exists. Please log in.", "warning")
            return render_template("signup.html", clerk_publishable_key=clerk_key)

        if models.get_user_by_phone(phone_number):
            flash("This phone number is already registered.", "warning")
            return render_template("signup.html", clerk_publishable_key=clerk_key)

        try:
            models.create_user(
                name, email, phone_number, password,
                int(age), gender, community, occupation, state
            )
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("main.login"))
        except Exception as e:
            flash(f"Error creating account: {e}", "danger")
            return render_template("signup.html", clerk_publishable_key=clerk_key)

    return render_template("signup.html", clerk_publishable_key=clerk_key)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    clerk_key = os.environ.get("CLERK_PUBLISHABLE_KEY", "")

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
            flash("Invalid email or password.", "danger")

    return render_template("login.html", clerk_publishable_key=clerk_key)


@bp.route("/api/auth/google", methods=["POST"])
def google_auth():
    """Handle Google Auth from Clerk SSO callback — syncs user with local DB."""
    data  = request.get_json(force=True) or {}
    name  = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()

    if not email:
        return jsonify({"error": "Missing email"}), 400

    # Fallback name from email prefix
    if not name:
        name = email.split("@")[0].replace(".", " ").title()

    try:
        user = models.get_or_create_google_user(name, email)
        if user:
            session["user_id"]   = user["id"]
            session["user_name"] = user["name"]
            return jsonify({
                "success": True,
                "redirect": url_for("main.dashboard"),
                "user_name": user["name"]
            }), 200
        else:
            return jsonify({"error": "Failed to create user"}), 500
    except Exception as e:
        print(f"[Google Auth Error] {e}")
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
        dl = s.get("deadline")
        if dl:
            if isinstance(dl, str):
                from datetime import datetime
                try:
                    dl = datetime.strptime(dl, "%Y-%m-%d").date()
                    s["deadline"] = dl
                except Exception:
                    dl = None
            s["status"] = "Expired" if dl and dl < current_date else "Active"
        else:
            s["status"] = "Active"

    return render_template("dashboard.html", user=user, schemes=eligible, today=date.today())


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
        dl = s.get("deadline")
        if dl:
            if isinstance(dl, str):
                from datetime import datetime
                try:
                    dl = datetime.strptime(dl, "%Y-%m-%d").date()
                    s["deadline"] = dl
                except Exception:
                    dl = None
            s["status"] = "Expired" if dl and dl < current_date else "Active"
        else:
            s["status"] = "Active"
    return render_template("admin.html", users=users, schemes=schemes)


@bp.route("/admin/user/delete/<int:user_id>", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    models.delete_user(user_id)
    flash("User deleted successfully.", "success")
    return redirect(url_for("main.admin_dashboard"))


@bp.route("/admin/scheme/upload-csv", methods=["GET", "POST"])
@admin_required
def admin_upload_csv():
    if request.method == "POST":
        import csv, io
        f = request.files.get("csv_file")
        if not f or not f.filename.endswith(".csv"):
            flash("Please upload a valid .csv file.", "danger")
            return redirect(url_for("main.admin_upload_csv"))

        stream = io.StringIO(f.stream.read().decode("utf-8-sig"), newline=None)
        reader = csv.DictReader(stream)

        added, skipped = 0, 0
        errors = []
        for i, row in enumerate(reader, start=2):
            try:
                models.add_scheme(
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
                skipped += 1
                errors.append(f"Row {i}: {e}")

        if added:
            flash(f"Successfully added {added} scheme(s).", "success")
        if skipped:
            flash(f"Skipped {skipped} row(s) due to errors: {'; '.join(errors[:3])}", "warning")

        # Notify users for all newly added schemes
        for s in models.get_all_schemes()[-added:] if added else []:
            notify_matching_users(s)

        return redirect(url_for("main.admin_dashboard"))

    return render_template("upload_csv.html")


@bp.route("/admin/scheme/sample-csv")
@admin_required
def download_sample_csv():
    from flask import Response
    sample = (
        "scheme_name,description,eligibility,community,min_age,max_age,max_income,"
        "benefits,documents_required,deadline,official_link\n"
        "PM Kisan Samman Nidhi,Financial support for farmers,"
        "Small and marginal farmers with cultivable land,All,18,70,0,"
        "₹6000/year in 3 installments,Aadhaar Card|Land Records|Bank Passbook,"
        "2025-12-31,https://pmkisan.gov.in\n"
        "Pudhumai Penn Scheme,Monthly stipend for girl students,"
        "Girls who studied Class 6-12 in TN govt schools now in higher education,"
        "All,18,30,0,₹1000/month stipend until graduation,"
        "School TC|College Admission Proof|Aadhaar|Bank Account,,https://tn.gov.in\n"
    )
    return Response(
        sample,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=sample_schemes.csv"}
    )


@bp.route("/admin/scheme/add", methods=["GET", "POST"])
@admin_required
def admin_add_scheme():
    if request.method == "POST":
        try:
            scheme_id = models.add_scheme(
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
            # Fire WhatsApp alerts to matching users in background
            new_scheme = models.get_scheme_by_id(scheme_id) if scheme_id else None
            if new_scheme:
                notify_matching_users(new_scheme)
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


# =============================================================================
# WEB SCRAPER — Real-time scheme updates
# =============================================================================

@bp.route("/api/scrape/schemes")
@admin_required
def scrape_schemes():
    """Scrape latest schemes from govt websites and return as JSON."""
    try:
        from scraper import run_scraper
        results = run_scraper()
        return jsonify({"count": len(results), "schemes": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/admin/scrape", methods=["GET", "POST"])
@admin_required
def admin_scrape():
    """Admin page to scrape and optionally import schemes."""
    if request.method == "POST":
        try:
            from scraper import run_scraper
            scraped = run_scraper()
            imported = 0
            for s in scraped:
                name = s.get("scheme_name", "").strip()
                if not name:
                    continue
                # Skip if already exists
                existing = [x for x in models.get_all_schemes() if x.get("scheme_name","").lower() == name.lower()]
                if existing:
                    continue
                try:
                    models.add_scheme(
                        name=name,
                        description=s.get("description",""),
                        eligibility=s.get("eligibility","All citizens"),
                        community=s.get("community","All"),
                        min_age=0, max_age=100, max_income=0,
                        benefits=s.get("benefits","See official link"),
                        documents="Aadhaar Card, Bank Account",
                        deadline=None,
                        link=s.get("official_link","https://india.gov.in"),
                    )
                    imported += 1
                except Exception:
                    pass
            flash(f"Scraped {len(scraped)} schemes, imported {imported} new ones.", "success")
        except Exception as e:
            flash(f"Scraping failed: {e}", "danger")
        return redirect(url_for("main.admin_dashboard"))
    return render_template("scrape.html")


# =============================================================================
# AI ELIGIBILITY SCORE  (Groq / Llama 3.3)
# =============================================================================

@bp.route("/api/eligibility-score", methods=["POST"])
def eligibility_score():
    """
    Accepts { scheme_id, scheme_name, eligibility, community, min_age, max_age }
    Returns  { score: int, reason: str }
    Uses Groq llama-3.3-70b. Falls back to rule-based if no API key.
    """
    if "user_id" not in session:
        return jsonify({"score": 70, "reason": "Not logged in"}), 200

    data = request.get_json(force=True) or {}
    user = models.get_user_by_id(session["user_id"])
    if not user:
        return jsonify({"score": 70, "reason": "Profile not found"}), 200

    scheme_name  = data.get("scheme_name", "")
    eligibility  = data.get("eligibility", "")
    community    = data.get("community", "All")
    min_age      = data.get("min_age", 0)
    max_age      = data.get("max_age", 100)

    # ── Rule-based fallback (instant, no API) ──────────────────
    def rule_score():
        score = 50
        reasons = []
        user_comm = user.get("community", "")
        comms = [c.strip() for c in community.split(",")]
        if "All" in comms or user_comm in comms:
            score += 25
            reasons.append("community matches")
        else:
            score -= 10
            reasons.append("community mismatch")
        age = int(user.get("age", 0))
        if min_age <= age <= max_age:
            score += 20
            reasons.append("age eligible")
        else:
            score -= 15
            reasons.append("age out of range")
        occ = user.get("occupation", "").lower()
        elig_lower = eligibility.lower()
        if any(w in elig_lower for w in [occ, "all", "any"]):
            score += 5
            reasons.append("occupation relevant")
        score = max(10, min(99, score))
        return score, ", ".join(reasons) if reasons else "Based on profile"

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        sc, reason = rule_score()
        return jsonify({"score": sc, "reason": reason}), 200

    prompt = f"""You are an eligibility checker for Indian government schemes.

User Profile:
- Age: {user.get('age')}
- Gender: {user.get('gender')}
- Community: {user.get('community')}
- Occupation: {user.get('occupation')}
- State: {user.get('state')}

Scheme: {scheme_name}
Eligibility Criteria: {eligibility}
Target Community: {community}
Age Range: {min_age} to {max_age}

Based on the user profile vs scheme criteria, return ONLY valid JSON (no markdown, no explanation outside JSON):
{{"score": <integer 0-100>, "reason": "<one short sentence why>"}}"""

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=80,
        )
        raw = resp.choices[0].message.content.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        import json as _json
        result = _json.loads(raw)
        score  = max(0, min(100, int(result.get("score", 70))))
        reason = str(result.get("reason", ""))[:120]
        return jsonify({"score": score, "reason": reason}), 200
    except Exception as e:
        print(f"[Groq Score Error] {e}")
        sc, reason = rule_score()
        return jsonify({"score": sc, "reason": reason}), 200


# =============================================================================
# WHATSAPP NOTIFICATIONS  (MSG91 — uses your existing key)
# =============================================================================

def send_whatsapp_alert(to_phone: str, scheme_name: str, benefits: str, link: str):
    """Send WhatsApp via MSG91. to_phone must be 10-digit Indian number."""
    auth_key = os.environ.get("MSG91_AUTH_KEY", "")

    if not auth_key:
        print(f"[WhatsApp] MSG91 not configured — skipping {to_phone}")
        return False

    # Skip dummy Google-signup phones
    if not to_phone or not to_phone.isdigit() or len(to_phone) != 10:
        return False

    try:
        # MSG91 WhatsApp API
        url = "https://api.msg91.com/api/v5/whatsapp/whatsapp-outbound-message/bulk/"
        body = (
            f"🎉 *New Scheme Alert — Schemo*\n\n"
            f"*{scheme_name}*\n"
            f"Benefits: {benefits[:200]}\n\n"
            f"Apply here: {link}\n\n"
            f"_Visit Schemo for more eligible schemes._"
        )
        payload = {
            "integrated_number": os.environ.get("MSG91_WHATSAPP_NUMBER", ""),
            "content_type": "template",
            "payload": {
                "to": f"91{to_phone}",
                "type": "text",
                "text": {"body": body}
            }
        }
        headers = {"authkey": auth_key, "Content-Type": "application/json"}
        import json as _json
        resp = requests.post(url, data=_json.dumps(payload), headers=headers, timeout=10)
        if resp.status_code == 200:
            print(f"[WhatsApp] Sent to +91{to_phone}")
            return True
        else:
            print(f"[WhatsApp] MSG91 error {resp.status_code}: {resp.text[:100]}")
            return False
    except Exception as e:
        print(f"[WhatsApp Error] {to_phone}: {e}")
        return False


def notify_matching_users(scheme: dict):
    """Background: find all users eligible for scheme and WhatsApp them."""
    import threading

    def _run():
        try:
            all_users = models.get_all_users()
            scheme_community = scheme.get("community", "All")
            comms = [c.strip() for c in scheme_community.split(",")]
            min_age = int(scheme.get("min_age", 0))
            max_age = int(scheme.get("max_age", 100))
            sent = 0
            for u in all_users:
                u_comm = u.get("community", "")
                u_age  = int(u.get("age", 0) or 0)
                phone  = u.get("phone_number", "")
                if "All" not in comms and u_comm not in comms:
                    continue
                if not (min_age <= u_age <= max_age):
                    continue
                ok = send_whatsapp_alert(
                    phone,
                    scheme.get("scheme_name", "New Scheme"),
                    scheme.get("benefits", ""),
                    scheme.get("official_link", "https://india.gov.in"),
                )
                if ok:
                    sent += 1
            print(f"[WhatsApp] Notified {sent} users for '{scheme.get('scheme_name')}'")
        except Exception as e:
            print(f"[WhatsApp Notify Error] {e}")

    threading.Thread(target=_run, daemon=True).start()
