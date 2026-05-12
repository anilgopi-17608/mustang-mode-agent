"""
================================================================
MUSTANG MODE - DAILY AI JOB AGENT (CLOUD + STATS v3.0)
================================================================
🆕 v3.0 Update:
- Saves real stats to stats.json after each run
- Stats are displayed on public landing page
================================================================
"""

import os
import re
import json
import time
import base64
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Optional: Gemini AI
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# =====================================================
# LOAD SECRETS FROM ENVIRONMENT VARIABLES
# =====================================================

try:
    from config import GMAIL_APP_PASSWORD as LOCAL_PASSWORD
except ImportError:
    LOCAL_PASSWORD = None

GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") or LOCAL_PASSWORD or ""
GMAIL_TOKEN_JSON = os.environ.get("GMAIL_TOKEN_JSON", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# =====================================================
# CONFIGURATION
# =====================================================

DIGEST_RECIPIENT = "anilgopi731@gmail.com"
SENDER_EMAIL = "anilgopi731@gmail.com"
SENDER_APP_PASSWORD = GMAIL_APP_PASSWORD

DAYS_BACK = 1
MAX_EMAILS = 100
MIN_MATCH_PCT = 20

USE_AI_BRAIN = bool(GEMINI_API_KEY) and GEMINI_AVAILABLE
MAX_AI_ANALYSES = 8
AI_DELAY_SECONDS = 1

# =====================================================
# ANIL'S PROFILE
# =====================================================

USER_NAME = "Anil"

USER_PROFILE_SUMMARY = """
Anil Gopi Gudapati - Mechanical Design Engineer / CAD Engineer
Location: Hyderabad, India
Education: B-Tech Mechanical Engineering (2024)
Experience: ~1 year
- CAD Engineer at restor3d: Designs patient-specific orthopedic implants
- AutoCAD Design Intern at HP Associates: HVAC systems

Core Skills: SolidWorks (expert), CATIA, AutoCAD, NX CAD, CERO, 3D modeling
Domain Expertise: Orthopedic implants, medical devices, weldment, HVAC, sheet metal
Career Stage: Early career, open to design engineer roles
Looking For: Mechanical/Design Engineer roles in Hyderabad/Remote
"""

USER_SKILLS = [
    "solidworks", "catia", "autocad", "nx cad", "nx", "cero", "creo",
    "cad", "cad modeling", "3d modeling", "drafting", "drawing",
    "mechanical", "mechanical engineering", "mechanical design",
    "design engineer", "design", "product design",
    "orthopedic", "implant", "patient-specific", "medical device",
    "weldment", "sheet metal", "hvac", "ductwork",
    "manufacturing", "production", "quality control", "qa", "qc",
    "ansys", "fea", "simulation", "gd&t",
    "automotive", "aerospace",
    "graduate engineer", "trainee", "intern", "junior engineer",
    "fresher", "entry level"
]

JOB_KEYWORDS = [
    "hiring", "job", "career", "vacancy", "opportunity",
    "recruitment", "position", "apply", "openings", "opening",
    "join our team", "we're hiring", "we are hiring",
    "naukri", "linkedin", "indeed", "foundit", "monster",
    "shortlisted", "your application", "interview",
    "engineer", "engineering", "designer"
]

PREFERRED_LOCATIONS = [
    "hyderabad", "telangana", "remote", "wfh", "work from home",
    "bangalore", "bengaluru", "chennai", "pune"
]

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
STATS_FILE = 'stats.json'

# =====================================================
# STATS MANAGEMENT
# =====================================================

def load_stats():
    """Load existing stats or create new structure"""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "last_run": None,
        "last_run_iso": None,
        "stats": {
            "total_runs": 0,
            "total_emails_scanned": 0,
            "total_jobs_matched": 0,
            "emails_scanned_7d": 0,
            "jobs_matched_7d": 0,
            "avg_match_score": 0,
            "high_match_count": 0
        },
        "recent_sources": {
            "linkedin": 0,
            "naukri": 0,
            "indeed": 0,
            "foundit": 0,
            "direct": 0
        },
        "history": []
    }


def save_stats(stats_data):
    """Save stats to JSON file"""
    with open(STATS_FILE, 'w') as f:
        json.dump(stats_data, f, indent=2)
    print(f"[OK] Stats saved to {STATS_FILE}")


def update_stats(matched_jobs, scanned_count):
    """Update stats with current run data"""
    stats = load_stats()
    now = datetime.now()
    
    # Increment counters
    stats["stats"]["total_runs"] += 1
    stats["stats"]["total_emails_scanned"] += scanned_count
    stats["stats"]["total_jobs_matched"] += len(matched_jobs)
    
    # Update last run
    stats["last_run"] = now.strftime("%B %d, %Y at %I:%M %p IST")
    stats["last_run_iso"] = now.isoformat()
    
    # Add to history (keep last 28 runs = 7 days x 4/day)
    history_entry = {
        "timestamp": now.isoformat(),
        "scanned": scanned_count,
        "matched": len(matched_jobs),
        "high_match": sum(1 for j in matched_jobs if j['match'] >= 70)
    }
    stats["history"].append(history_entry)
    if len(stats["history"]) > 28:
        stats["history"] = stats["history"][-28:]
    
    # Compute 7-day stats from history
    seven_days_ago = now - timedelta(days=7)
    recent_runs = [h for h in stats["history"] 
                   if datetime.fromisoformat(h["timestamp"]) >= seven_days_ago]
    
    stats["stats"]["emails_scanned_7d"] = sum(h["scanned"] for h in recent_runs)
    stats["stats"]["jobs_matched_7d"] = sum(h["matched"] for h in recent_runs)
    stats["stats"]["high_match_count"] = sum(h["high_match"] for h in recent_runs)
    
    # Average match score from current run
    if matched_jobs:
        avg = sum(j['match'] for j in matched_jobs) / len(matched_jobs)
        stats["stats"]["avg_match_score"] = int(avg)
    
    # Source breakdown
    for job in matched_jobs:
        sender = job.get('subject', '').lower() + job.get('company', '').lower()
        if 'linkedin' in sender:
            stats["recent_sources"]["linkedin"] += 1
        elif 'naukri' in sender:
            stats["recent_sources"]["naukri"] += 1
        elif 'indeed' in sender:
            stats["recent_sources"]["indeed"] += 1
        elif 'foundit' in sender or 'monster' in sender:
            stats["recent_sources"]["foundit"] += 1
        else:
            stats["recent_sources"]["direct"] += 1
    
    save_stats(stats)
    return stats


# =====================================================
# GEMINI AI BRAIN
# =====================================================

def init_gemini():
    if not USE_AI_BRAIN:
        return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("[OK] Gemini AI brain activated")
        return model
    except Exception as e:
        print(f"[WARN] Gemini init failed: {e}")
        return None


def ai_analyze_job(model, job_data):
    if not model:
        return None

    prompt = f"""You are a career advisor analyzing a job for this candidate:

{USER_PROFILE_SUMMARY}

JOB DETAILS:
Title: {job_data['title']}
Company: {job_data['company']}
Location: {job_data['location']}
Salary: {job_data['salary']}
Description: {job_data['preview'][:600]}

Analyze this job for THIS specific candidate. Respond ONLY with valid JSON:

{{
    "ai_score": <integer 0-100>,
    "verdict": "<HIGH|GOOD|SKIP>",
    "reasoning": "<2 sentences explaining fit>",
    "concerns": "<one concern or 'None'>",
    "cover_opener": "<one sentence cover letter opener>"
}}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith('```'):
            text = re.sub(r'^```(?:json)?\s*', '', text)
            text = re.sub(r'\s*```$', '', text)
        return json.loads(text)
    except Exception as e:
        print(f"  [AI] Failed: {e}")
        return None


# =====================================================
# GMAIL API
# =====================================================

def gmail_authenticate():
    creds = None
    if GMAIL_TOKEN_JSON:
        try:
            token_data = json.loads(GMAIL_TOKEN_JSON)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
            print("[OK] Loaded credentials from environment variable")
        except Exception as e:
            print(f"[WARN] Failed to load token from env: {e}")

    if not creds and os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        print("[OK] Loaded credentials from token.json file")

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        print("[OK] Refreshed expired credentials")

    if not creds or not creds.valid:
        raise RuntimeError("No valid credentials found!")

    return build('gmail', 'v1', credentials=creds)


def get_full_email_body(payload):
    body_text = ""
    if 'parts' in payload:
        for part in payload['parts']:
            mime = part.get('mimeType', '')
            if mime in ('text/plain', 'text/html'):
                data = part.get('body', {}).get('data', '')
                if data:
                    body_text += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            if 'parts' in part:
                body_text += get_full_email_body(part)
    else:
        data = payload.get('body', {}).get('data', '')
        if data:
            body_text += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

    body_text = re.sub(r'<[^>]+>', ' ', body_text)
    body_text = re.sub(r'\s+', ' ', body_text)
    return body_text


def get_header(headers, name):
    for h in headers:
        if h.get('name', '').lower() == name.lower():
            return h.get('value', '')
    return ''


def extract_salary(text):
    patterns = [
        r'rs\.?\s?[\d,]+(?:\.\d+)?\s?(?:lpa|lakhs?|lac|cr|crore|k)?',
        r'inr\s?[\d,]+(?:\.\d+)?\s?(?:lpa|lakhs?|lac|cr|crore|k)?',
        r'\$\s?[\d,]+(?:\.\d+)?\s?(?:k|per\s?annum|/year)?',
        r'[\d]+\s?-\s?[\d]+\s?(?:lpa|lakhs?|lac|k)',
        r'[\d]+(?:\.\d+)?\s?(?:lpa|lakhs?|lac|cr|crore)',
        r'ctc\s?:?\s?[\d,]+(?:\.\d+)?\s?(?:lpa|lakhs?|lac|k)?',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(0).upper()
    return "Not Mentioned"


def extract_location(text):
    found = []
    for city in PREFERRED_LOCATIONS:
        if city in text.lower():
            found.append(city.title())
    if found:
        return ", ".join(set(found))
    other_cities = ["mumbai", "delhi", "noida", "gurgaon", "kolkata", "ahmedabad",
                    "kochi", "coimbatore", "indore", "jaipur", "vizag"]
    for city in other_cities:
        if city in text.lower():
            return city.title()
    return "Not Mentioned"


def extract_apply_link(text):
    patterns = [
        r'https?://[^\s<>"]+(?:apply|career|job|view)[^\s<>"]*',
        r'https?://(?:www\.)?(?:linkedin|naukri|indeed|foundit|monster)[^\s<>"]*',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(0)
    return None


def extract_company(subject, sender):
    sender_clean = sender.split('<')[0].strip().replace('"', '')
    if sender_clean and '@' not in sender_clean:
        for suffix in [' Talent', ' Recruitment', ' Careers', ' HR', ' Team', ' Jobs', ' Notifications']:
            if suffix.lower() in sender_clean.lower():
                sender_clean = re.sub(suffix, '', sender_clean, flags=re.IGNORECASE).strip()
        return sender_clean[:35] if sender_clean else "Recruiter"
    return "Recruiter"


def extract_job_title(subject, body):
    titles = [
        "design engineer", "mechanical engineer", "cad engineer",
        "automotive engineer", "r&d engineer", "product engineer",
        "manufacturing engineer", "simulation engineer", "fea engineer",
        "drafting engineer", "aerospace engineer", "production engineer",
        "quality engineer", "graduate engineer", "trainee engineer",
        "design trainee", "junior engineer", "associate engineer"
    ]
    text = (subject + " " + body[:500]).lower()
    for t in titles:
        if t in text:
            return t.title()
    return subject[:60] if subject else "Engineering Role"


def calculate_match(text, user_skills):
    matched = [s for s in user_skills if s in text.lower()]
    if not matched:
        return 0, []
    pct = int((len(matched) / max(len(user_skills), 1)) * 100)
    return min(pct * 3, 100), matched


def is_job_email(text):
    text_lower = text.lower()
    return any(kw in text_lower for kw in JOB_KEYWORDS)


def location_priority_boost(location):
    loc = location.lower()
    if "hyderabad" in loc:
        return 15
    if any(c in loc for c in ["remote", "wfh", "work from home"]):
        return 12
    if any(c in loc for c in ["bangalore", "bengaluru", "chennai", "pune"]):
        return 5
    return 0


def scan_gmail():
    print("Connecting to Gmail...")
    service = gmail_authenticate()

    after_date = (datetime.now() - timedelta(days=DAYS_BACK)).strftime('%Y/%m/%d')
    query = (
        f'after:{after_date} '
        '(hiring OR job OR career OR vacancy OR opportunity OR '
        'recruitment OR engineer OR mechanical OR design OR '
        'solidworks OR autocad OR catia OR position OR '
        'naukri OR linkedin OR indeed OR foundit)'
    )

    print(f"Scanning emails from past {DAYS_BACK} day(s)...")

    all_messages = []
    next_page = None
    while len(all_messages) < MAX_EMAILS:
        req = {'userId': 'me', 'q': query, 'maxResults': min(100, MAX_EMAILS - len(all_messages))}
        if next_page:
            req['pageToken'] = next_page
        results = service.users().messages().list(**req).execute()
        msgs = results.get('messages', [])
        all_messages.extend(msgs)
        next_page = results.get('nextPageToken')
        if not next_page or not msgs:
            break

    print(f"Found {len(all_messages)} candidate emails")

    matched_jobs = []

    for idx, msg in enumerate(all_messages):
        try:
            txt = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        except Exception as e:
            print(f"  Skipped: {e}")
            continue

        payload = txt.get('payload', {})
        headers = payload.get('headers', [])
        subject = get_header(headers, 'subject') or 'No Subject'
        sender = get_header(headers, 'from')
        snippet = txt.get('snippet', '')
        full_body = get_full_email_body(payload)
        full_text = f"{subject} {snippet} {full_body}"

        if not is_job_email(full_text):
            continue

        match_pct, matched_skills = calculate_match(full_text, USER_SKILLS)
        location = extract_location(full_body or snippet)
        match_pct += location_priority_boost(location)
        match_pct = min(match_pct, 100)

        if match_pct < MIN_MATCH_PCT:
            continue

        salary = extract_salary(full_body or snippet)
        link = extract_apply_link(full_body)
        company = extract_company(subject, sender)
        title = extract_job_title(subject, full_body)

        matched_jobs.append({
            'subject': subject[:80],
            'company': company,
            'title': title,
            'location': location,
            'salary': salary,
            'match': match_pct,
            'matched_skills': matched_skills,
            'preview': full_body[:500] if full_body else snippet,
            'link': link,
            'ai_analysis': None
        })

        print(f"  Match #{len(matched_jobs)}: {title} @ {company} ({match_pct}%)")

    matched_jobs.sort(key=lambda x: x['match'], reverse=True)
    return matched_jobs, len(all_messages)


def enrich_with_ai(matched_jobs):
    if not USE_AI_BRAIN:
        return matched_jobs
    model = init_gemini()
    if not model:
        return matched_jobs
    top_jobs = matched_jobs[:MAX_AI_ANALYSES]
    print(f"[AI] Analyzing top {len(top_jobs)} jobs with Gemini...")
    for i, job in enumerate(top_jobs):
        analysis = ai_analyze_job(model, job)
        if analysis:
            job['ai_analysis'] = analysis
        time.sleep(AI_DELAY_SECONDS)
    def sort_key(j):
        if j.get('ai_analysis'):
            return j['ai_analysis']['ai_score']
        return j['match']
    matched_jobs.sort(key=sort_key, reverse=True)
    return matched_jobs


def build_digest_html(jobs, scanned_count):
    today = datetime.now().strftime("%A, %B %d, %Y")
    if not jobs:
        body_html = """
        <div style='text-align:center; padding:60px 30px; background:#ffffff; border:1px solid #e5e7eb; border-radius:12px;'>
            <div style='font-size:48px; margin-bottom:10px;'>🏁</div>
            <h2 style='color:#dc2626; font-family:Verdana; margin:0 0 10px 0;'>NO NEW MATCHES TODAY</h2>
            <p style='color:#6b7280; margin:0;'>The inbox was quiet today. Check again tomorrow!</p>
        </div>
        """
    else:
        job_cards = ""
        for i, j in enumerate(jobs[:10], 1):
            skills_html = " ".join([
                f"<span style='background:#fee2e2; border:1px solid #fca5a5; color:#991b1b; padding:4px 12px; border-radius:15px; font-size:11px; margin-right:5px; display:inline-block; margin-bottom:5px; font-weight:600;'>+ {s.title()}</span>"
                for s in j['matched_skills'][:6]
            ])
            apply_btn = ""
            if j['link']:
                apply_btn = f"""
                <a href='{j['link']}' style='display:inline-block; background:linear-gradient(135deg,#dc2626,#991b1b); color:#ffffff; padding:11px 24px; border-radius:8px; text-decoration:none; font-family:Verdana, Arial, sans-serif; font-weight:bold; font-size:12px; letter-spacing:1.5px; margin-top:14px;'>ENTER RACE &nbsp;&rarr;</a>
                """
            preview_clean = j['preview'].replace('<', '&lt;').replace('>', '&gt;')[:220]
            ai_html = ""
            ai = j.get('ai_analysis')
            if ai:
                verdict = ai['verdict']
                if verdict == 'HIGH':
                    verdict_color = '#16a34a'
                    verdict_emoji = '🔥'
                    verdict_label = 'HIGHLY RECOMMENDED'
                elif verdict == 'GOOD':
                    verdict_color = '#dc2626'
                    verdict_emoji = '👍'
                    verdict_label = 'WORTH APPLYING'
                else:
                    verdict_color = '#f59e0b'
                    verdict_emoji = '🤷'
                    verdict_label = 'SKIP'
                concerns_html = ""
                if ai.get('concerns') and ai['concerns'].lower() not in ['none', '']:
                    concerns_html = f"<div style='margin-top:8px; padding:8px; background:#fef3c7; border-left:3px solid #f59e0b; border-radius:4px; font-size:12px; color:#78350f;'><b>⚠️ Concern:</b> {ai['concerns']}</div>"
                cover_html = ""
                if ai.get('cover_opener'):
                    cover_html = f"<div style='margin-top:8px; padding:10px; background:#dbeafe; border-left:3px solid #2563eb; border-radius:4px; font-size:12px; color:#1e3a8a; font-style:italic;'><b>✍️ Cover letter opener:</b><br>\"{ai['cover_opener']}\"</div>"
                ai_html = f"""
                <div style='margin-top:12px; padding:14px; background:#f0fdf4; border:1px solid #86efac; border-radius:8px;'>
                    <div style='font-size:11px; color:{verdict_color}; font-weight:bold;'>🧠 AI VERDICT: {verdict_emoji} {verdict_label} (Score: {ai['ai_score']}/100)</div>
                    <div style='font-size:13px; color:#111; line-height:1.5; margin-top:6px;'>{ai['reasoning']}</div>
                    {concerns_html}
                    {cover_html}
                </div>
                """
            display_score = ai['ai_score'] if ai else j['match']
            if display_score >= 70:
                match_color = "#16a34a"
                match_label = "HIGH MATCH"
            elif display_score >= 50:
                match_color = "#dc2626"
                match_label = "GOOD MATCH"
            else:
                match_color = "#f59e0b"
                match_label = "POTENTIAL"
            job_cards += f"""
            <div style='background:#ffffff; border:1px solid #e5e7eb; border-left:4px solid #dc2626; border-radius:12px; padding:22px; margin-bottom:16px;'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;'>
                    <div style='flex:1;'>
                        <div style='font-size:10px; color:#9ca3af; letter-spacing:2px; font-weight:bold;'>POLE POSITION #{i} &nbsp;|&nbsp; <span style='color:{match_color};'>{match_label}</span></div>
                        <div style='color:#111827; font-size:18px; font-weight:bold; margin-top:6px;'>{j['title']}</div>
                        <div style='color:#dc2626; font-size:13px; font-weight:bold;'>{j['company']}</div>
                    </div>
                    <span style='background:linear-gradient(135deg,#dc2626,#991b1b); color:#ffffff; padding:7px 16px; border-radius:20px; font-size:13px; font-weight:bold;'>{display_score}%</span>
                </div>
                <div style='color:#4b5563; font-size:13px; margin:12px 0;'>📍 <b style='color:#111827;'>{j['location']}</b> | 💰 <b style='color:#111827;'>{j['salary']}</b></div>
                <div style='color:#6b7280; font-size:12.5px; margin:10px 0; padding:12px; background:#f9fafb; border-left:3px solid #dc2626; border-radius:4px;'>{preview_clean}...</div>
                <div style='margin-top:10px;'>{skills_html}</div>
                {ai_html}
                {apply_btn}
            </div>
            """
        body_html = job_cards
    high_match_count = sum(1 for j in jobs if (j.get('ai_analysis', {}) or {}).get('ai_score', j['match']) >= 70)
    html = f"""
    <html><body style='margin:0; padding:0; background:#f3f4f6; font-family:Verdana, Arial, sans-serif;'>
        <div style='max-width:700px; margin:0 auto; padding:24px 16px;'>
            <div style='text-align:center; padding:32px 20px; background:linear-gradient(135deg, #1f1f1f, #0a0a0a); border-radius:16px; margin-bottom:20px;'>
                <div style='color:#dc2626; font-size:36px; font-weight:bold; letter-spacing:4px;'>🏎️ MUSTANG MODE</div>
                <h1 style='color:#ffffff; letter-spacing:6px; margin:8px 0 0 0; font-size:18px;'>DAILY DIGEST</h1>
                <div style='color:#9ca3af; font-size:11px; letter-spacing:2px; margin-top:8px;'>{today.upper()}</div>
            </div>
            <div style='background:#ffffff; border-radius:12px; padding:20px 24px; margin-bottom:18px; border:1px solid #e5e7eb;'>
                <div style='color:#111827; font-size:15px;'>Good morning <span style='color:#dc2626; font-weight:bold;'>{USER_NAME}</span>! 👋<br>Found <b style='color:#16a34a;'>{len(jobs)} jobs</b> from {scanned_count} emails ({high_match_count} high-priority).</div>
            </div>
            {body_html}
            <div style='text-align:center; padding:24px; margin-top:20px; background:#1f1f1f; border-radius:12px;'>
                <div style='color:#dc2626; font-size:11px; letter-spacing:3px; font-weight:bold;'>TUNED BY PRECISION · DRIVEN BY ENGINEERING</div>
            </div>
        </div></body></html>
    """
    return html


def send_digest(html_content, job_count):
    if not SENDER_APP_PASSWORD:
        print("ERROR: No GMAIL_APP_PASSWORD!")
        return False
    today = datetime.now().strftime("%b %d")
    subject = f"🏎️ Mustang Mode v3 | {job_count} jobs analyzed ({today})"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"Mustang Mode AI <{SENDER_EMAIL}>"
    msg['To'] = DIGEST_RECIPIENT
    msg.attach(MIMEText(html_content, 'html'))
    print(f"Sending to {DIGEST_RECIPIENT}...")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)
        print("Sent successfully!")
        return True
    except Exception as e:
        print(f"Send failed: {e}")
        return False


def main():
    print("=" * 60)
    print("MUSTANG MODE v3.0 - WITH REAL STATS")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    matched_jobs, scanned_count = scan_gmail()

    print("")
    print("=" * 60)
    print(f"SCAN RESULT: {len(matched_jobs)} matches from {scanned_count} emails")
    print("=" * 60)

    if matched_jobs:
        matched_jobs = enrich_with_ai(matched_jobs)

    html = build_digest_html(matched_jobs, scanned_count)
    send_digest(html, len(matched_jobs))

    # ⭐ NEW: Update stats.json with this run's data
    print("")
    print("Updating public stats...")
    update_stats(matched_jobs, scanned_count)
    
    print("Daily run complete.")


if __name__ == "__main__":
    main()
