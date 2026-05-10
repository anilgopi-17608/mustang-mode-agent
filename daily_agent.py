"""
================================================================
MUSTANG MODE - DAILY AI JOB AGENT
================================================================
Tuned for: ANIL GOPI GUDAPATI
Profile : Mechanical Design Engineer / CAD Engineer
Location: Hyderabad

Runs once a day, scans Gmail for new jobs matching your profile,
and emails you a beautifully formatted digest.
================================================================

USAGE:
    python daily_agent.py

SCHEDULE (Windows Task Scheduler):
    Set this script to run daily at 7:00 AM
================================================================
"""

import os
import re
import base64
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# =====================================================
# CONFIGURATION - edit these for your setup
# =====================================================

DIGEST_RECIPIENT = "anilgopi731@gmail.com"
SENDER_EMAIL = "anilgopi731@gmail.com"
SENDER_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "piffajrpftbcfeyw")

DAYS_BACK = 1
MAX_EMAILS = 100
MIN_MATCH_PCT = 20

# =====================================================
# ANIL'S PROFILE
# =====================================================

USER_NAME = "Anil"

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

# =====================================================
# GMAIL API
# =====================================================

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

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
            print(f"  Skipped one email: {e}")
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
            'preview': full_body[:250] if full_body else snippet,
            'link': link
        })

        print(f"  Match #{len(matched_jobs)}: {title} @ {company} ({match_pct}%)")

    matched_jobs.sort(key=lambda x: x['match'], reverse=True)
    return matched_jobs, len(all_messages)


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
                <a href='{j['link']}' style='display:inline-block; background:linear-gradient(135deg,#dc2626,#991b1b); color:#ffffff; padding:11px 24px; border-radius:8px; text-decoration:none; font-family:Verdana, Arial, sans-serif; font-weight:bold; font-size:12px; letter-spacing:1.5px; margin-top:14px; box-shadow:0 2px 8px rgba(220,38,38,0.3);'>ENTER RACE &nbsp;&rarr;</a>
                """

            preview_clean = j['preview'].replace('<', '&lt;').replace('>', '&gt;')[:220]

            # Match color logic
            if j['match'] >= 70:
                match_color = "#16a34a"   # green for high match
                match_label = "HIGH MATCH"
            elif j['match'] >= 50:
                match_color = "#dc2626"   # red for good match
                match_label = "GOOD MATCH"
            else:
                match_color = "#f59e0b"   # amber for low match
                match_label = "POTENTIAL"

            job_cards += f"""
            <div style='background:#ffffff; border:1px solid #e5e7eb; border-left:4px solid #dc2626; border-radius:12px; padding:22px; margin-bottom:16px; box-shadow:0 1px 3px rgba(0,0,0,0.05);'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;'>
                    <div style='flex:1;'>
                        <div style='font-size:10px; color:#9ca3af; letter-spacing:2px; font-family:Verdana, Arial, sans-serif; font-weight:bold;'>POLE POSITION #{i} &nbsp;|&nbsp; <span style='color:{match_color};'>{match_label}</span></div>
                        <div style='font-family:Verdana, Arial, sans-serif; color:#111827; font-size:18px; font-weight:bold; margin-top:6px; line-height:1.3;'>{j['title']}</div>
                        <div style='color:#dc2626; font-size:13px; font-weight:bold; margin-top:3px;'>{j['company']}</div>
                    </div>
                    <span style='background:linear-gradient(135deg,#dc2626,#991b1b); color:#ffffff; padding:7px 16px; border-radius:20px; font-size:13px; font-weight:bold; font-family:Verdana, Arial, sans-serif; min-width:50px; text-align:center; flex-shrink:0; margin-left:12px;'>{j['match']}%</span>
                </div>
                <div style='color:#4b5563; font-size:13px; margin:12px 0; padding:6px 0; border-top:1px solid #f3f4f6; border-bottom:1px solid #f3f4f6;'>
                    📍 <b style='color:#111827;'>{j['location']}</b> &nbsp;&nbsp;|&nbsp;&nbsp; 💰 <b style='color:#111827;'>{j['salary']}</b>
                </div>
                <div style='color:#6b7280; font-size:12.5px; line-height:1.6; margin:10px 0; padding:12px; background:#f9fafb; border-left:3px solid #dc2626; border-radius:4px;'>{preview_clean}...</div>
                <div style='margin-top:10px;'>{skills_html}</div>
                {apply_btn}
            </div>
            """

        body_html = job_cards

    high_match_count = sum(1 for j in jobs if j['match'] >= 50)

    html = f"""
    <html>
    <body style='margin:0; padding:0; background:#f3f4f6; font-family:Verdana, Arial, sans-serif;'>
        <div style='max-width:700px; margin:0 auto; background:#f3f4f6; padding:24px 16px;'>

            <!-- HEADER -->
            <div style='text-align:center; padding:32px 20px; background:linear-gradient(135deg, #1f1f1f 0%, #0a0a0a 100%); border-radius:16px; margin-bottom:20px; box-shadow:0 4px 12px rgba(0,0,0,0.15);'>
                <div style='color:#dc2626; font-size:36px; margin-bottom:6px; font-weight:bold; letter-spacing:4px; font-family:Verdana, Arial, sans-serif;'>🏎️ MUSTANG MODE</div>
                <h1 style='color:#ffffff; font-family:Verdana, Arial, sans-serif; letter-spacing:6px; margin:8px 0 0 0; font-size:18px; font-weight:bold;'>DAILY DIGEST</h1>
                <div style='color:#9ca3af; font-size:11px; letter-spacing:2px; margin-top:8px;'>{today.upper()}</div>
            </div>

            <!-- GREETING -->
            <div style='background:#ffffff; border-radius:12px; padding:20px 24px; margin-bottom:18px; border:1px solid #e5e7eb; box-shadow:0 1px 3px rgba(0,0,0,0.04);'>
                <div style='color:#111827; font-size:15px; line-height:1.7;'>
                    Good morning <span style='color:#dc2626; font-weight:bold;'>{USER_NAME}</span>! 👋<br>
                    Your AI agent scanned <b style='color:#111827;'>{scanned_count} emails</b> overnight and found
                    <b style='color:#16a34a;'>{len(jobs)} jobs</b> matching your profile
                    ({high_match_count} are high-match).
                </div>
            </div>

            <!-- METRICS -->
            <table style='width:100%; border-collapse:separate; border-spacing:8px 0; margin-bottom:20px;'>
                <tr>
                    <td style='width:33%; background:#ffffff; border:1px solid #e5e7eb; padding:16px 8px; border-radius:10px; text-align:center;'>
                        <div style='color:#111827; font-size:24px; font-weight:bold; font-family:Verdana, Arial, sans-serif;'>{scanned_count}</div>
                        <div style='color:#6b7280; font-size:10px; letter-spacing:1.5px; font-weight:600;'>SCANNED</div>
                    </td>
                    <td style='width:33%; background:#ffffff; border:1px solid #e5e7eb; padding:16px 8px; border-radius:10px; text-align:center;'>
                        <div style='color:#dc2626; font-size:24px; font-weight:bold; font-family:Verdana, Arial, sans-serif;'>{len(jobs)}</div>
                        <div style='color:#6b7280; font-size:10px; letter-spacing:1.5px; font-weight:600;'>MATCHED</div>
                    </td>
                    <td style='width:33%; background:#ffffff; border:1px solid #e5e7eb; padding:16px 8px; border-radius:10px; text-align:center;'>
                        <div style='color:#16a34a; font-size:24px; font-weight:bold; font-family:Verdana, Arial, sans-serif;'>{high_match_count}</div>
                        <div style='color:#6b7280; font-size:10px; letter-spacing:1.5px; font-weight:600;'>POLE POSITION</div>
                    </td>
                </tr>
            </table>

            <!-- JOB CARDS -->
            {body_html}

            <!-- FOOTER -->
            <div style='text-align:center; padding:24px 20px; margin-top:20px; background:#1f1f1f; border-radius:12px;'>
                <div style='color:#dc2626; font-size:11px; letter-spacing:3px; font-family:Verdana, Arial, sans-serif; font-weight:bold;'>TUNED BY PRECISION &nbsp;|&nbsp; DRIVEN BY ENGINEERING</div>
                <div style='margin-top:10px; color:#6b7280; font-size:10px; letter-spacing:1px;'>🏎️ Mustang Mode AI Agent &nbsp;·&nbsp; Sent automatically every morning</div>
            </div>

        </div>
    </body>
    </html>
    """
    return html


def send_digest(html_content, job_count):
    if SENDER_APP_PASSWORD == "":
        print("")
        print("WARNING: No email password set!")
        print("Email NOT sent. See setup guide for App Password.")
        print("")
        print("Saving digest to 'last_digest.html' for preview...")
        with open('last_digest.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Open 'last_digest.html' in your browser to preview.")
        print("")
        return

    today = datetime.now().strftime("%b %d")
    subject = f"Mustang Mode | {job_count} jobs found today ({today})"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"Mustang Mode <{SENDER_EMAIL}>"
    msg['To'] = DIGEST_RECIPIENT

    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)

    print(f"Sending digest to {DIGEST_RECIPIENT}...")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            server.send_message(msg)
        print("Digest sent successfully!")
    except Exception as e:
        print(f"Send failed: {e}")
        print("Saving digest to 'last_digest.html' as backup...")
        with open('last_digest.html', 'w', encoding='utf-8') as f:
            f.write(html_content)


def main():
    print("=" * 60)
    print("MUSTANG MODE - DAILY AGENT")
    print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Driver: {USER_NAME}")
    print("=" * 60)

    matched_jobs, scanned_count = scan_gmail()

    print("")
    print("=" * 60)
    print(f"SCAN RESULT: {len(matched_jobs)} matches from {scanned_count} emails")
    print("=" * 60)

    html = build_digest_html(matched_jobs, scanned_count)
    send_digest(html, len(matched_jobs))

    print("Daily run complete.")


if __name__ == "__main__":
    main()