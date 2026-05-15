# 🏎️ MUSTANG MODE — Complete Project Documentation

**Last Updated:** May 15, 2026  
**Built by:** Anil Gopi Gudapati  
**Project Status:** ✅ FULLY DEPLOYED & LIVE

---

## 📋 PROJECT OVERVIEW

**Mustang Mode** is a multi-agent AI system that includes:

1. **🏎️ Job Agent** — Scans Gmail 4× daily for engineering jobs, summarizes with Gemini AI, sends beautiful email digests
2. **🌅 News Agent** — Daily morning digest with tech news, market data, medical device news
3. **🌐 Public Landing Page** — Beautiful website showcasing the project (live on GitHub Pages)
4. **📰 News Page** — Separate page with collapsible accordion sections for daily news

---

## 🔗 LIVE PRODUCTION LINKS

| Resource | URL |
|---|---|
| **🌐 Landing Page** | https://anilgopi-17608.github.io/mustang-mode-agent/ |
| **📰 News Page** | https://anilgopi-17608.github.io/mustang-mode-agent/news.html |
| **📦 GitHub Repo (Public)** | https://github.com/anilgopi-17608/mustang-mode-agent |
| **💼 LinkedIn** | https://www.linkedin.com/in/anil-gopi-gudapati |
| **🐙 GitHub Profile** | https://github.com/anilgopi-17608 |

---

## 👤 USER PROFILE

- **Name:** Anil Gopi Gudapati
- **Role:** Mechanical Design Engineer / CAD Engineer
- **Current Company:** restor3d (Hyderabad) - Patient-specific orthopedic implants
- **Education:** B-Tech Mechanical Engineering (KHIT Guntur, 2024)
- **Location:** Hyderabad, India
- **Email:** anilgopi731@gmail.com
- **GitHub Username:** anilgopi-17608
- **Core Skills:** SolidWorks, CATIA, AutoCAD, NX CAD, CERO, orthopedic design, weldment, HVAC

---

## 🛠️ COMPLETE TECH STACK

### Backend / Agent
- **Python 3.11** — Both agents
- **Gmail API** — Reading emails (OAuth 2.0)
- **SMTP** — Sending emails (Gmail App Password)
- **Google Gemini 1.5 Flash** — AI summaries and job scoring
- **Yahoo Finance API** — Live stock market data

### Cloud Infrastructure
- **GitHub Actions** — Cron-based scheduling
- **GitHub Pages** — Free static hosting
- **GitHub Secrets** — Encrypted credentials storage

### Frontend
- **Pure HTML/CSS** — No frameworks
- **Vanilla JavaScript** — Dynamic data loading
- **Google Fonts** — Audiowide (headings), Inter (body)
- **CSS Grid + Flexbox** — Responsive layout
- **Backdrop-filter blur** — Frosted glass effects

### Design System
- **Primary Colors:** #ffd700 (gold) → #ff6b00 (orange) → #dc2626 (red)
- **Background:** #0a0014 (deep purple), BMW M5 Competition image
- **Theme:** Racing/automotive, premium tech feel

---

## 📁 COMPLETE REPO FILE STRUCTURE

```
mustang-mode-agent/
├── .github/
│   └── workflows/
│       ├── mustang.yml          # Job agent workflow (4× daily)
│       └── news.yml             # News agent workflow (7 AM IST)
├── .gitignore
├── BMW M5 Competition.jpg       # Landing page background image
├── README.md
├── daily_agent.py               # Job scanner (v3.0 with stats)
├── index.html                   # Landing page
├── news.html                    # News digest page
├── news-icon.png                # Globe icon for news button
├── news.json                    # Auto-updated news data
├── news_agent.py                # News aggregator
├── requirements.txt             # Python dependencies
└── stats.json                   # Auto-updated job stats
```

---

## ⏰ SCHEDULED WORKFLOWS

### Job Agent (`mustang.yml`)
**Schedule:** UTC times for IST conversion
- **02:30 UTC** = 8:00 AM IST
- **04:30 UTC** = 10:00 AM IST  
- **06:30 UTC** = 12:00 PM IST
- **13:30 UTC** = 7:00 PM IST

**What it does:**
1. Authenticates to Gmail via OAuth token
2. Searches last 24 hours for job emails
3. Extracts: job title, company, location, salary
4. Calculates skill match score
5. Top 8 jobs get Gemini AI analysis with verdict + cover letter opener
6. Builds beautiful HTML digest
7. Sends via SMTP to anilgopi731@gmail.com
8. Updates `stats.json` with run statistics
9. Auto-commits `stats.json` to repo

### News Agent (`news.yml`)
**Schedule:** 01:30 UTC = 7:00 AM IST daily

**What it does:**
1. Fetches RSS feeds from multiple sources
2. Pulls live stock data from Yahoo Finance
3. Gemini AI summarizes each article
4. Builds HTML email digest
5. Sends to anilgopi731@gmail.com
6. Saves all data to `news.json`
7. Auto-commits `news.json` to repo

---

## 📰 NEWS SOURCES (RSS Feeds)

### 🤖 AI & Tech (5 stories)
- TechCrunch
- The Verge
- Ars Technica
- MIT Technology Review

### 💼 Market Intelligence (5 stories) — Deals, Acquisitions, Business
- Economic Times Markets
- Moneycontrol Business
- Business Standard Markets
- Livemint Companies
- Reuters Business

### 🏥 Medical Devices (3 stories) — Anil's Industry
- MassDevice
- Medical Design & Outsourcing
- Medical Device Network

### 🇮🇳 India Tech (3 stories)
- YourStory
- Inc42
- Entrackr

### 🛠️ Engineering (2 stories)
- Design World
- Engineering.com

### 📺 YouTube Channels (videos)
- MKBHD (Marques Brownlee)
- Two Minute Papers (AI)

### 📈 Stock Market Data (Yahoo Finance)
- **Indices:** Nifty 50, Sensex, Bank Nifty
- **Currency:** USD/INR
- **Commodity:** Gold (₹/10g)
- **Top Stocks Tracked:** TCS, Reliance, HDFC Bank, Infosys, ICICI Bank, L&T, Wipro, Maruti, Sun Pharma, Bharti Airtel

---

## 🔐 GITHUB SECRETS (Configured)

These secrets are set in: Settings → Secrets and variables → Actions

| Secret Name | Purpose |
|---|---|
| `GMAIL_APP_PASSWORD` | 16-char Gmail App Password for SMTP |
| `GMAIL_TOKEN_JSON` | OAuth token for Gmail API reading |
| `GEMINI_API_KEY` | Google AI Studio API key |

⚠️ **Security:** Secrets are encrypted by GitHub. Even with public repo, no one can see these values.

---

## 🎨 LANDING PAGE FEATURES

### Top Navigation
- 🏎️ **Mustang Mode** brand logo (Audiowide font, gradient)
- **Nav links:** How it works, Features, Stack
- 👤 **Avatar pill:** "AG Anil →" linking to LinkedIn
- 🌍 **Globe icon button:** Opens news page in new tab

### Hero Section
- **Pill:** "⚡ Autonomous AI Job Agent"
- **Title:** "The AI that Hunts Jobs While I Sleep"
- **Tagline:** "🏁 TUNED BY PRECISION · DRIVEN BY ENGINEERING 🏁"
- **Right side tag lines** (clickable, opens news page):
  - "here are some market updates →" + preview data
  - "here are some tech updates →" + preview data

### Visual Elements
- **BMW M5 Competition background** (fixed, cinematic overlay)
- **Racing stripe** at top (animated gradient)
- **Vignette effect** on edges
- **Frosted glass cards** throughout

### CTA Buttons
- "📦 View on GitHub →" → Repo
- "📧 See Sample Email" → Anchor link

### Stats Row (Live)
- Total Runs (from stats.json)
- Jobs Matched (7d)
- Emails Scanned (7d)
- Avg Match Score

### Source Filter Tabs
- 🌐 All Jobs (filter)
- 💼 LinkedIn → opens linkedin.com/jobs/
- 🇮🇳 Naukri → opens naukri.com/mynaukri/
- 🔍 Indeed → opens in.indeed.com/myjobs
- ✉️ Direct (filter)

### Other Sections
- How it Works (4 steps)
- Features (6 cards)
- Tech Stack (10 badges)

---

## 📰 NEWS PAGE FEATURES (news.html)

### Layout
- **Sticky nav** with brand + "← Back to Home" button
- **Page header** with date and "LAST UPDATED" timestamp
- **6 collapsible accordion sections** (click arrow → expand)

### Sections (all collapsible)
1. **📈 MARKET SNAPSHOT** — Auto-opens on page load
   - Indices grid (Nifty, Sensex, Bank Nifty)
   - Currency (USD/INR)
   - Commodity (Gold)
   - Top 3 Gainers
   - Top 3 Losers

2. **🤖 AI & TECH** — 3 stories with AI summaries
3. **💼 MARKET INTELLIGENCE** — Deals, IPOs, acquisitions
4. **🏥 MEDICAL DEVICES** — Your field
5. **🇮🇳 INDIA TECH** — Indian startup news
6. **🛠️ ENGINEERING** — CAD/manufacturing news

### Dynamic Loading
- Fetches `news.json` on page load
- Shows loading spinner while fetching
- Empty state if no data yet
- Updates daily after news agent runs

---

## 📧 EMAIL DIGEST DESIGN (Job Agent)

### Visual Style
- **Theme:** Light (cream background) for readability
- **Cards:** White with red Mustang accent border
- **Font:** Verdana for email compatibility

### Per Job Card Contains
- **Pole Position #X** label
- **Match badge:** Green ≥70% (HIGH), Red 50-69% (GOOD), Amber <50% (POTENTIAL)
- **Source badge:** Color-coded (LinkedIn blue, Naukri orange, Indeed blue, Direct purple)
- **Job title + Company**
- **Location & Salary** (extracted with regex)
- **Match preview** (snippet from email)
- **Skill tags** (matched skills as colored pills)
- **🧠 AI VERDICT** (for top 8 jobs):
  - AI Score (0-100)
  - Verdict: HIGHLY RECOMMENDED / WORTH APPLYING / SKIP
  - Reasoning (2 sentences)
  - Concerns (red flags)
  - ✍️ Cover letter opener (copy-paste ready)
- **"ENTER RACE →" button** (link to job application)

### Email Header
```
🏎️ MUSTANG MODE
DAILY DIGEST
[DATE]
```

### Email Footer
```
🏁 TUNED BY PRECISION · DRIVEN BY ENGINEERING 🏁
```

---

## 🧠 JOB MATCHING LOGIC

### Skills Tracked (35+)
```python
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
```

### Match Score Calculation
```python
base_score = min((matched_skills / total_skills) * 3 * 100, 100)
location_boost = 15 if "hyderabad" else 12 if "remote" else 5 if other_india_city else 0
final_score = min(base_score + location_boost, 100)
```

### Filters
- **MIN_MATCH_PCT:** 20% (minimum to include in digest)
- **DAYS_BACK:** 1 day (only scan last 24 hours)
- **MAX_EMAILS:** 100 per scan
- **MAX_AI_ANALYSES:** 8 jobs get full AI verdict

---

## 📊 DATA FILES

### stats.json (auto-updated)
Tracks all job agent runs:
```json
{
  "last_run": "May 15, 2026 at 7:00 AM IST",
  "last_run_iso": "2026-05-15T07:00:00",
  "stats": {
    "total_runs": 28,
    "total_emails_scanned": 247,
    "total_jobs_matched": 42,
    "emails_scanned_7d": 89,
    "jobs_matched_7d": 12,
    "avg_match_score": 78,
    "high_match_count": 5
  },
  "recent_sources": {
    "linkedin": 8,
    "naukri": 5,
    "indeed": 18,
    "foundit": 2,
    "direct": 1
  },
  "history": [...]
}
```

### news.json (auto-updated)
Stores latest news + market data for the landing page and news page:
```json
{
  "last_updated": "Thursday, May 15, 2026 at 7:00 AM IST",
  "market": {
    "indices": [...],
    "currency": [...],
    "commodity": [...],
    "gainers": [...],
    "losers": [...]
  },
  "categories": {
    "🤖 AI & TECH": { "items": [...] },
    "💼 MARKET INTELLIGENCE": { "items": [...] },
    "🏥 MEDICAL DEVICES": { "items": [...] },
    "🇮🇳 INDIA TECH": { "items": [...] },
    "🛠️ ENGINEERING": { "items": [...] }
  }
}
```

---

## 🔄 INTEGRATION FLOW

```
┌─────────────────────────────────────────────────────────┐
│  GitHub Actions (Cron Scheduler)                        │
│  ├─ mustang.yml: 4× daily                              │
│  └─ news.yml: 1× daily at 7 AM IST                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Python Agents                                          │
│  ├─ daily_agent.py: Scan Gmail → Score → Send digest   │
│  └─ news_agent.py: Fetch RSS + Yahoo → Send digest     │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────┐         ┌──────────────────┐
│  Gmail       │         │  Update JSON     │
│  Send Email  │         │  - stats.json    │
│  (SMTP)      │         │  - news.json     │
└──────────────┘         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Auto-commit     │
                         │  to GitHub repo  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  GitHub Pages    │
                         │  Serves files    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Landing Page    │
                         │  Fetches JSON    │
                         │  Shows live data │
                         └──────────────────┘
```

---

## ✅ COMPLETE FEATURE CHECKLIST

### Job Agent
- [x] Gmail OAuth integration
- [x] Last 24-hour email scan
- [x] Regex-based job email detection
- [x] Skill matching (35+ skills)
- [x] Salary extraction (Indian + USD formats)
- [x] Location detection with boost (Hyderabad +15%, Remote +12%)
- [x] Gemini AI scoring (top 8 jobs)
- [x] AI-generated verdicts (HIGH/GOOD/SKIP)
- [x] AI-generated concerns
- [x] AI-generated cover letter openers
- [x] Beautiful HTML email digest
- [x] 4× daily scheduling via GitHub Actions
- [x] Live stats tracking (stats.json)
- [x] Auto-commit stats after each run

### News Agent
- [x] Multi-source RSS feed parsing
- [x] Atom feed support (YouTube)
- [x] Yahoo Finance integration
- [x] Indian markets (Nifty, Sensex, Bank Nifty)
- [x] Top gainers/losers tracking
- [x] USD/INR + Gold prices
- [x] Gemini AI summaries
- [x] HTML email digest
- [x] Daily 7 AM IST scheduling
- [x] Saves news.json
- [x] Auto-commit news data

### Landing Page (index.html)
- [x] BMW M5 Competition background
- [x] Mustang fire color theme (yellow → orange → red)
- [x] Audiowide racing font
- [x] Sticky navigation
- [x] Nav avatar pill linking to LinkedIn
- [x] Globe icon button for news (opens news.html in new tab)
- [x] Hero section with title and tagline
- [x] Right-side tag lines (market + tech previews)
- [x] Live previews pulling from news.json
- [x] CTA buttons (GitHub + Sample Email)
- [x] Stats row (live from stats.json)
- [x] Source filter tabs (LinkedIn/Naukri/Indeed/Direct)
- [x] How It Works section (4 steps)
- [x] Features section (6 cards)
- [x] Tech Stack section (10 badges)
- [x] Footer
- [x] Mobile responsive

### News Page (news.html)
- [x] Same Mustang theme
- [x] "← Back to Home" link
- [x] Date timestamp + last updated indicator
- [x] Collapsible accordion sections
- [x] Market Snapshot section (auto-opens)
- [x] AI & Tech section
- [x] Market Intelligence section
- [x] Medical Devices section
- [x] India Tech section
- [x] Engineering section
- [x] Dynamic loading from news.json
- [x] Loading spinner
- [x] Empty state if no data
- [x] Mobile responsive

### Infrastructure
- [x] GitHub repo (public)
- [x] GitHub Pages deployment
- [x] GitHub Actions workflows
- [x] GitHub Secrets (3 configured)
- [x] Auto-commit permissions
- [x] .gitignore protecting credentials
- [x] OAuth token in env variable

---

## 📂 LOCAL DEVELOPMENT FILES (User's Computer)

These files are on Anil's computer (C:\Users\anilg\OneDrive\Desktop\AI_JOB_AGENT\) but NOT on GitHub:

```
AI_JOB_AGENT/
├── Resume/Anil Gopi CV.pdf
├── app.py                    # Streamlit dashboard (not deployed)
├── credentials.json          # Google OAuth client credentials (SECRET!)
├── token.json                # Gmail OAuth token (SECRET!)
├── token_backup.json
├── config.py                 # Contains GMAIL_APP_PASSWORD (SECRET!)
├── generate_token.py         # Used to regenerate Gmail OAuth token
├── run_mustang.bat           # Windows batch wrapper
├── last_digest.html
└── last_run.log
```

**Important:** These files contain SECRETS and are gitignored. They never go to GitHub.

---

## 🚀 NEXT STEPS / FUTURE IDEAS

Things that could be built next:

### Quick Wins
- [ ] Add Anil's resume PDF as featured download
- [ ] Add a "Subscribe to digest" form (for others)
- [ ] Add testimonials section
- [ ] Add demo video

### Feature Additions
- [ ] WhatsApp alerts for HIGH match jobs (via Twilio)
- [ ] Streamlit dashboard polish (use existing app.py)
- [ ] Full cover letter generator (currently just openers)
- [ ] Job application tracker
- [ ] Add more sources (Naukri RSS, LinkedIn API alternatives)
- [ ] Sentiment analysis on emails
- [ ] Job market trends dashboard
- [ ] Salary negotiation suggestions

### Engineering Improvements
- [ ] Unit tests for matchers
- [ ] Better error handling
- [ ] Retry logic for failed API calls
- [ ] Caching for stock data
- [ ] Optimize Gmail queries

### Product Expansion
- [ ] Multi-user version (others can sign up)
- [ ] Custom skills per user
- [ ] User dashboard with login
- [ ] Premium tier with more features
- [ ] Mobile app (React Native)

---

## 🐛 KNOWN ISSUES / GOTCHAS

1. **Browser downloads add numbers:** `news.html (1).html` etc — must rename to exactly `news.html` before uploading
2. **Filename case-sensitivity:** GitHub Pages requires exact case match
3. **Caching:** Use `Ctrl+Shift+R` to bypass browser cache after deploys
4. **Rate limits:** Gmail rate-limits multiple test runs in short period (normal behavior)
5. **News.json updates:** Only refresh after workflow runs (daily at 7 AM IST or manual trigger)

---

## 💬 USER COMMUNICATION STYLE

Anil prefers:
- 🎯 Step-by-step numbered instructions
- 📋 Visual diagrams when explaining concepts
- 💪 Encouragement and racing/automotive metaphors
- 🏎️ Emojis (especially 🏎️🔥)
- ELI5 explanations (no jargon)
- Asking before making big changes
- Testing in stages

Anil's skill level:
- Beginner Python coder
- Strong with mechanical engineering
- Telugu/Hindi/English speaker (sometimes makes typos)
- Sometimes shares passwords in screenshots (always need to warn)

---

## 🏆 BUILD TIMELINE

- **Day 1:** Built basic agent with ChatGPT, switched to Claude
- **Day 2:** UI redesign, Windows Task Scheduler automation
- **Day 3:** GitHub Actions cloud deployment, Gemini AI integration  
- **Day 4:** Public landing page with BMW M5 background
- **Day 5:** Source-filtered tabs, AG nav avatar
- **Day 6:** Live stats integration, News agent v1
- **Day 7:** News page with collapsible sections, tag lines

**Result:** Production-deployed AI system + portfolio site

---

## 🎯 CRITICAL INFO FOR CONTINUATION

If you're continuing this project (in a new Claude account or with another developer):

### Things you NEED to know:
1. The repo is **public**: anilgopi-17608/mustang-mode-agent
2. All secrets are in **GitHub Secrets** (encrypted)
3. Schedules use **UTC time** (subtract 5:30 for IST)
4. Gmail uses both **OAuth (reading) and App Password (sending)**
5. Files auto-commit back via **GitHub Actions write permissions**

### Common commands:
```bash
# View files in repo
https://github.com/anilgopi-17608/mustang-mode-agent

# Run workflow manually
Actions tab → workflow name → "Run workflow"

# Check live site
https://anilgopi-17608.github.io/mustang-mode-agent/
```

### If something breaks:
1. Check **Actions tab** for error logs
2. Check **GitHub Secrets** are still configured
3. Check **Permissions** in repo Settings → Actions
4. Verify file paths and filenames are exact match

---

## 🌟 FINAL STATUS (May 15, 2026)

```
🏆 MUSTANG MODE — PRODUCTION DEPLOYED 🏆
═══════════════════════════════════════════════════════

✅ Job Agent running 24/7 (cloud)
✅ News Agent running daily at 7 AM IST
✅ Beautiful public landing page LIVE
✅ News page with collapsible sections LIVE
✅ Live stats updating automatically
✅ Live news data updating automatically
✅ All deployments stable
✅ Zero cost to operate (₹0/month)

📊 Public URL: https://anilgopi-17608.github.io/mustang-mode-agent/
📦 Code: https://github.com/anilgopi-17608/mustang-mode-agent
📧 Receiving daily digests at: anilgopi731@gmail.com
```

---

> 🏎️ **TUNED BY PRECISION · DRIVEN BY ENGINEERING** 🏁
> 
> Built in 7 days by Anil Gopi Gudapati, Mechanical Design Engineer  
> Powered by Python, Claude AI, Gemini AI, and a lot of coffee ☕

---

**End of Project Documentation**
