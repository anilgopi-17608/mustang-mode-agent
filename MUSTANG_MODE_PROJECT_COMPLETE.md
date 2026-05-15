# 🏎️ MUSTANG MODE — Complete Project Documentation v2.0

**Last Updated:** May 15, 2026  
**Built by:** Anil Gopi Gudapati  
**Project Status:** ✅ FULLY DEPLOYED & LIVE  
**Total AI Agents:** 3 (Job Agent, News Agent, Market Updater)

---

## 📋 PROJECT OVERVIEW

**Mustang Mode** is a multi-agent AI system that includes:

1. **🏎️ Job Agent** — Scans Gmail 4× daily for engineering jobs, summarizes with Gemini AI, sends beautiful email digests
2. **🌅 News Agent** — Daily morning digest with tech news + medical devices news
3. **📈 Market Updater (NEW!)** — Hourly market data refresh (Indian + US + Crypto)
4. **🌐 Public Landing Page** — Beautiful website showcasing the project
5. **📰 News Page** — Separate page with collapsible accordion sections

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
- **Education:** B.Tech Mechanical Engineering (KHIT Guntur, 2024)
- **Location:** Hyderabad, India
- **Email:** anilgopi731@gmail.com
- **GitHub Username:** anilgopi-17608
- **Core Skills:** SolidWorks, CATIA, AutoCAD, NX CAD, CERO, orthopedic design

---

## 🛠️ COMPLETE TECH STACK

### Backend / Agents
- **Python 3.11**
- **Gmail API** — OAuth 2.0 for reading emails
- **SMTP** — Gmail App Password for sending
- **Google Gemini 1.5 Flash** — AI summaries and job scoring
- **Yahoo Finance API** — Live stock data (Indian + US + Crypto)

### Cloud Infrastructure
- **GitHub Actions** — Cron-based scheduling
- **GitHub Pages** — Free static hosting
- **GitHub Secrets** — Encrypted credentials

### Frontend
- **Pure HTML/CSS** — No frameworks
- **Vanilla JavaScript** — Dynamic data loading + auto-refresh
- **Google Fonts** — Audiowide (headings), Inter (body)
- **Backdrop-filter blur** — Frosted glass effects

### Design System
- **Colors:** #ffd700 (gold) → #ff6b00 (orange) → #dc2626 (red)
- **Background:** #0a0014 (deep purple), BMW M5 image
- **Theme:** Racing/automotive, premium tech

---

## 📁 COMPLETE REPO FILE STRUCTURE (UPDATED)

```
mustang-mode-agent/
├── .github/
│   └── workflows/
│       ├── mustang.yml          # Job agent (4× daily)
│       ├── news.yml             # News agent (7 AM IST)
│       └── market.yml           # ⭐ NEW! Market updater (hourly)
├── .gitignore
├── BMW M5 Competition.jpg       # Landing page background
├── README.md
├── daily_agent.py               # Job scanner (v3.0)
├── index.html                   # Landing page
├── market_agent.py              # ⭐ NEW! Market updater
├── news.html                    # News digest page
├── news-icon.png                # Globe icon
├── news.json                    # Auto-updated by news + market agents
├── news_agent.py                # News aggregator
├── requirements.txt
└── stats.json                   # Job stats (auto-updated)
```

---

## ⏰ ALL SCHEDULED WORKFLOWS

### 🏎️ Job Agent (`mustang.yml`)
**Schedule:** 4 times daily
- 02:30 UTC = 8:00 AM IST
- 04:30 UTC = 10:00 AM IST
- 06:30 UTC = 12:00 PM IST
- 13:30 UTC = 7:00 PM IST

**Actions:**
- Authenticates to Gmail via OAuth
- Searches last 24 hours for job emails
- Calculates skill match scores
- Top 8 jobs get Gemini AI analysis
- Builds HTML digest, sends email
- Updates `stats.json`
- Auto-commits to repo

### 🌅 News Agent (`news.yml`)
**Schedule:** Daily at 7:00 AM IST (01:30 UTC)

**Actions:**
- Fetches RSS feeds from 10+ sources
- Gemini AI summarizes each article
- Builds HTML email digest, sends
- Updates entire `news.json` (news + initial market)
- Auto-commits to repo

### 📈 Market Updater (`market.yml`) — NEW!
**Schedule:** Every hour, 24/7 (`'0 * * * *'`)

**Actions:**
- Fetches Indian indices (5)
- Fetches Indian stocks (12) → calculates gainers/losers
- Fetches US indices (3) + US stocks (7)
- Fetches Crypto (4 coins)
- Fetches Currency + Commodity
- Updates ONLY market section of `news.json`
- NO emails sent
- Auto-commits to repo

---

## 📊 MARKET DATA TRACKED (NEW EXPANDED!)

### 🇮🇳 INDIAN MARKETS

**Indices (5):**
- Nifty 50, Sensex, Bank Nifty, Nifty IT, Nifty Pharma

**Stocks Tracked (12):**
- TCS, Reliance, HDFC Bank, Infosys, ICICI Bank
- L&T, Wipro, Maruti, Sun Pharma, Bharti Airtel
- Bajaj Finance, Tata Motors

**Auto-calculated:**
- Top 3 Gainers
- Top 3 Losers

### 🇺🇸 US MARKETS

**Indices (3):**
- S&P 500, NASDAQ, Dow Jones

**Stocks (7):**
- Apple, Microsoft, Google, Nvidia, Tesla, Amazon, Meta

### ₿ CRYPTOCURRENCY (4)
- Bitcoin (BTC-USD)
- Ethereum (ETH-USD)
- Solana (SOL-USD)
- Cardano (ADA-USD)

### 💵 CURRENCY (2)
- USD/INR
- EUR/USD

### 🪙 COMMODITY (3)
- Gold (₹/10g)
- Silver
- Crude Oil

---

## 📰 NEWS SOURCES (RSS Feeds)

### 🤖 AI & Tech (5 stories)
- TechCrunch
- The Verge
- Ars Technica
- MIT Technology Review

### 💼 Market Intelligence (5 stories)
- Economic Times Markets
- Moneycontrol Business
- Business Standard
- Livemint Companies
- Reuters Business

### 🏥 Medical Devices (3 stories)
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

### 📺 YouTube (Videos)
- MKBHD
- Two Minute Papers

---

## 🔐 GITHUB SECRETS

| Secret Name | Purpose |
|---|---|
| `GMAIL_APP_PASSWORD` | 16-char Gmail App Password for SMTP |
| `GMAIL_TOKEN_JSON` | OAuth token for Gmail API reading |
| `GEMINI_API_KEY` | Google AI Studio API key |

---

## 🎨 LANDING PAGE FEATURES

- 🏎️ Mustang Mode brand (Audiowide font, gradient)
- BMW M5 Competition fixed background with overlay
- Racing stripe at top (animated)
- 👤 Avatar pill → LinkedIn
- 🌍 Globe icon → opens news page (new tab)
- Right-side floating tag lines:
  - "here are some market updates →" + live preview
  - "here are some tech updates →" + live preview
- Stats row (live from stats.json)
- Source filter tabs with platform shortcut arrows
- How It Works (4 steps)
- Features grid
- Tech Stack badges
- Mobile responsive

---

## 📰 NEWS PAGE FEATURES (UPDATED)

### Layout
- Sticky nav with brand + "← Back to Home"
- Page header with date
- **3 status indicators:**
  - "🟢 NEWS UPDATED: [time]" (daily)
  - "📈 MARKETS UPDATED: [time]" (hourly, animated blink)
- 6 collapsible accordion sections

### Sections (all collapsible)

1. **📈 MARKET SNAPSHOT** — Auto-opens, updates HOURLY
   - 🇮🇳 Indian Indices (5)
   - 🏆 Indian Gainers (top 3)
   - 📉 Indian Losers (top 3)
   - 🇺🇸 US Indices (3)
   - 📊 Top US Stocks (7)
   - ₿ Crypto (4)
   - 💵 Forex + Commodity (5)
   
   **TOTAL: 30+ indicators!**

2. **🤖 AI & TECH** — Daily news
3. **💼 MARKET INTELLIGENCE** — Daily news
4. **🏥 MEDICAL DEVICES** — Daily news
5. **🇮🇳 INDIA TECH** — Daily news
6. **🛠️ ENGINEERING** — Daily news

### Auto-Refresh
- Page auto-refreshes data every **5 minutes**
- Always shows latest market data
- No manual refresh needed!

---

## 📧 EMAIL DIGEST DESIGN

### Job Agent Email
- Light theme with fire accents
- Subject: `🏎️ Mustang Mode v2 | X jobs analyzed (Date)`
- Per job: source badge, match badge, AI verdict, cover letter opener

### News Agent Email
- Subject: `🌅 Tech Pit Stop | X stories + market update`
- Sections: AI/Tech, Market Intelligence, Medical Devices, India Tech, Engineering
- Initial market data included
- Beautiful HTML with category color-coding

---

## 🔄 INTEGRATION FLOW (UPDATED)

```
┌─────────────────────────────────────────────────────────┐
│  GitHub Actions (Cron Scheduler)                        │
│  ├─ mustang.yml: 4× daily (job emails)                 │
│  ├─ news.yml: 1× daily at 7 AM IST (news emails)       │
│  └─ market.yml: 24× daily, every hour (market updates) │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Python Agents                                          │
│  ├─ daily_agent.py: Job scanner                        │
│  ├─ news_agent.py: News + initial market               │
│  └─ market_agent.py: Hourly market refresh ⭐NEW       │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴──────────────┐
        ▼                           ▼
┌──────────────┐         ┌──────────────────────┐
│  Gmail SMTP  │         │  Update JSON Files   │
│  Send emails │         │  - stats.json (jobs) │
└──────────────┘         │  - news.json (news+  │
                         │    market)           │
                         └──────────┬───────────┘
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
                         │  Serves website  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────────┐
                         │  Landing & News      │
                         │  Pages fetch JSON    │
                         │  every 5 min         │
                         │  Show live data!     │
                         └──────────────────────┘
```

---

## ✅ COMPLETE FEATURE CHECKLIST

### Job Agent (Mustang)
- [x] Gmail OAuth integration
- [x] Skill matching (35+ skills)
- [x] Salary extraction (Indian + USD)
- [x] Location boost (Hyderabad +15%, Remote +12%)
- [x] Gemini AI scoring for top 8 jobs
- [x] Cover letter opener generation
- [x] 4× daily scheduling
- [x] Live stats tracking
- [x] Auto-commit stats.json

### News Agent (Tech Pit Stop)
- [x] Multi-source RSS parsing
- [x] Atom feed support (YouTube)
- [x] Gemini AI summaries
- [x] HTML email digest
- [x] Daily 7 AM IST scheduling
- [x] Saves news.json
- [x] Auto-commit news data

### Market Updater (NEW!)
- [x] Indian indices (5)
- [x] Indian stocks (12) + gainers/losers
- [x] US indices (3) + stocks (7)
- [x] Crypto (4 coins)
- [x] Forex (2)
- [x] Commodity (3)
- [x] Hourly schedule (24×/day)
- [x] No emails (just data)
- [x] Auto-commit news.json

### Landing Page (index.html)
- [x] BMW M5 background
- [x] Mustang fire theme
- [x] Globe icon → news page
- [x] Tag lines with live previews
- [x] Live stats from stats.json
- [x] Source filter tabs
- [x] Mobile responsive

### News Page (news.html)
- [x] Same Mustang theme
- [x] "Back to Home" link
- [x] Date + last-updated indicators
- [x] News updated indicator
- [x] Markets updated indicator (animated)
- [x] 6 collapsible sections
- [x] Indian Markets section
- [x] US Markets section (NEW!)
- [x] Crypto section (NEW!)
- [x] Forex + Commodity
- [x] News categories
- [x] Auto-refresh every 5 min
- [x] Mobile responsive

### Infrastructure
- [x] GitHub repo (public)
- [x] GitHub Pages deployment
- [x] 3 GitHub Actions workflows
- [x] 3 GitHub Secrets configured
- [x] Auto-commit permissions on all workflows

---

## 📊 DATA FILES STRUCTURE

### stats.json
```json
{
  "last_run": "May 15, 2026 at 7:00 AM IST",
  "stats": {
    "total_runs": 28,
    "total_emails_scanned": 247,
    "total_jobs_matched": 42,
    "emails_scanned_7d": 89,
    "jobs_matched_7d": 12,
    "avg_match_score": 78
  },
  "recent_sources": {...},
  "history": [...]
}
```

### news.json (UPDATED structure!)
```json
{
  "last_updated": "Thursday, May 15, 2026 at 7:00 AM IST",
  "market_last_updated": "2:00 PM IST",
  "market": {
    "indian": {
      "indices": [...],
      "gainers": [...],
      "losers": [...]
    },
    "us": {
      "indices": [...],
      "gainers": [...],
      "losers": [...]
    },
    "crypto": [...],
    "currency": [...],
    "commodity": [...]
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

## 🚀 NEXT STEPS / FUTURE IDEAS

### Quick Wins
- [ ] Add Anil's resume PDF as download
- [ ] Stock alerts (DM when stock crosses threshold)
- [ ] Email me when crypto pumps >5%
- [ ] Add favorites/watchlist

### Feature Additions
- [ ] WhatsApp alerts for HIGH match jobs
- [ ] Streamlit dashboard (existing app.py)
- [ ] Full cover letter generator
- [ ] Job application tracker
- [ ] Sentiment analysis on news

### Engineering Improvements
- [ ] Unit tests for matchers
- [ ] Better error handling
- [ ] Retry logic for failed API calls
- [ ] Caching for stock data
- [ ] WebSocket for real-time stock updates

### Product Expansion
- [ ] Multi-user version (others sign up)
- [ ] Custom skills per user
- [ ] Premium tier
- [ ] Mobile app

---

## 🐛 KNOWN ISSUES / GOTCHAS

1. **Filename downloads:** Browsers add numbers (`news.html (1).html`) — must rename
2. **Case-sensitivity:** GitHub Pages requires exact filename case
3. **Caching:** Use `Ctrl+Shift+R` for hard refresh after deploys
4. **Market hours:** US markets show stale data when US markets are closed (normal)
5. **Rate limits:** Yahoo Finance may rate-limit if too many requests too fast

---

## 💬 USER COMMUNICATION STYLE

**Anil prefers:**
- 🎯 Step-by-step numbered instructions
- 📋 Visual diagrams when explaining
- 💪 Racing/automotive metaphors
- 🏎️ Emojis (especially 🏎️🔥)
- ELI5 explanations
- Asking before major changes
- Testing in stages

**Skill level:**
- Beginner Python
- Strong with mechanical engineering
- Telugu/Hindi/English speaker

---

## 🏆 BUILD TIMELINE

- **Day 1:** Built basic agent with ChatGPT, switched to Claude
- **Day 2:** UI redesign, Task Scheduler automation
- **Day 3:** GitHub Actions deployment, Gemini AI integration
- **Day 4:** Public landing page with BMW M5
- **Day 5:** Source filter tabs, nav avatar
- **Day 6:** Live stats integration
- **Day 7:** News agent v1
- **Day 8:** News page with collapsible sections
- **Day 9:** Hourly market updater (Indian + US + Crypto) ⭐

---

## 🎯 CRITICAL INFO FOR CONTINUATION

### Things you NEED to know:
1. Repo is **public**: anilgopi-17608/mustang-mode-agent
2. Secrets are in **GitHub Secrets** (encrypted)
3. Schedules use **UTC time** (subtract 5:30 for IST)
4. Gmail uses both **OAuth + App Password**
5. Files auto-commit via **workflow write permissions**
6. 3 agents total: **mustang.yml**, **news.yml**, **market.yml**

### Quick references:
```bash
# View files
https://github.com/anilgopi-17608/mustang-mode-agent

# Run any workflow manually
Actions tab → workflow name → "Run workflow"

# Live site
https://anilgopi-17608.github.io/mustang-mode-agent/

# Check market updates
https://anilgopi-17608.github.io/mustang-mode-agent/news.html
```

### If something breaks:
1. Check **Actions tab** for error logs
2. Verify **GitHub Secrets** are configured
3. Check **Permissions** (Settings → Actions → Workflow permissions)
4. Verify filenames are exact case match

---

## 🌟 FINAL STATUS (May 15, 2026)

```
🏆 MUSTANG MODE — PRODUCTION DEPLOYED 🏆
═══════════════════════════════════════════════════════

✅ Job Agent running 24/7 (4× daily)
✅ News Agent running daily at 7 AM IST
✅ Market Updater running EVERY HOUR ⭐ NEW
✅ Beautiful public landing page LIVE
✅ News page with live markets LIVE
✅ Live stats auto-updating
✅ Live news data auto-updating  
✅ Live market data hourly updates
✅ All deployments stable
✅ Zero cost to operate (₹0/month)

📊 Public URL: https://anilgopi-17608.github.io/mustang-mode-agent/
📦 Code: https://github.com/anilgopi-17608/mustang-mode-agent
📧 Daily digests: anilgopi731@gmail.com

🌐 LIVE TRACKING:
   🇮🇳 5 Indian indices + 12 stocks
   🇺🇸 3 US indices + 7 stocks
   ₿ 4 cryptocurrencies
   💵 2 currency pairs + 3 commodities
   📰 16 daily news stories
   = 50+ data points refreshing automatically!
```

---

> 🏎️ **TUNED BY PRECISION · DRIVEN BY ENGINEERING** 🏁
>
> Built in 9 days by Anil Gopi Gudapati, Mechanical Design Engineer  
> Powered by Python, Claude AI, Gemini AI, Yahoo Finance, and a lot of coffee ☕

---

**End of Project Documentation v2.0**
