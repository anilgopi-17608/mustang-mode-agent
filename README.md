# 🏎️ Mustang Mode — AI Job Agent

> **TUNED BY PRECISION · DRIVEN BY ENGINEERING**

An autonomous AI agent that scans my Gmail every day, finds engineering jobs matching my profile, and emails me a beautifully formatted digest of the best matches.

---

## 🎯 What it does

Every day at **8 AM, 10 AM, 12 PM, 7 PM IST**, this agent:

1. 🔌 Connects to my Gmail via OAuth
2. 🔍 Scans the last 24 hours of emails
3. 🎯 Filters for job-related content
4. 🧠 Matches against my engineering skills (SolidWorks, CATIA, AutoCAD, NX CAD)
5. 📊 Calculates match % per job (with location boost for Hyderabad)
6. 💰 Extracts salary, location, apply links
7. 📧 Sends me a beautiful HTML digest with the top picks

---

## 🛠️ Tech stack

- **Python 3.11**
- **Gmail API** (OAuth 2.0)
- **SMTP** for sending HTML emails
- **GitHub Actions** for scheduling (runs in cloud, 24/7)
- **Regex** for salary/location extraction
- **HTML/CSS** for email design

---

## 🚀 Features

- ✅ **Skill-based matching** — uses my real resume skills
- ✅ **Location intelligence** — boosts Hyderabad/Remote/Bangalore
- ✅ **Match % scoring** — High Match / Good Match / Potential
- ✅ **Salary extraction** — Indian + international formats (LPA, CTC, ₹, $)
- ✅ **Apply links** — auto-extracted from email body
- ✅ **Fully autonomous** — runs in cloud, no manual trigger needed

---

## 🔒 Security

Secrets stored in **GitHub Actions secrets** (not in code):
- `GMAIL_APP_PASSWORD` — for sending emails
- `GMAIL_TOKEN_JSON` — for reading inbox

`config.py`, `token.json`, `credentials.json` are gitignored.

---

## 👨‍💻 Built by

**Anil Gopi Gudapati** — Mechanical Design Engineer
🌐 [LinkedIn](https://www.linkedin.com/in/anil-gopi-gudapati)

---

> 🔥 *Built in one day. Runs forever.* 🏎️
