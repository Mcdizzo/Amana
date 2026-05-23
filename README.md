# Amana

> *Mcheza Kwao Hutunzwa.*

Amana is a Tanzanian investment platform that makes government bond investing accessible to every Tanzanian — at home or abroad. No broker visits, no paperwork, no financial jargon. Just clear guidance in Swahili and a simple path to investing in Tanzania's future.

---

## What It Does

- **Landing page** — waitlist collection with WhatsApp share mechanic
- **Jifunze (/jifunze)** — step-by-step education on government bonds, CDS accounts, auctions, and a live return calculator
- **Auction tracker** — real BOT treasury bond auctions displayed in plain Swahili
- **Admin panel (/admin)** — manage auctions, view waitlist signups, read contact messages

---

## Tech Stack

- Python / Flask
- SQLite
- Vanilla HTML, CSS, JavaScript
- Deployed on Railway

---

## Project Structure

amana/
├── app.py
├── templates/
│   ├── index.html
│   ├── jifunze.html
│   └── admin.html
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── jifunze.css
│   │   └── admin.css
│   └── js/
│       ├── main.js
│       └── jifunze.js
└── amana.db

---

## Running Locally

```bash
pip install flask
python app.py
```

Visit `http://localhost:5000`

---

## Roadmap

- **Phase C** ✅ — Landing page and waitlist
- **Phase A** ✅ — Education and auction tracker  
- **Phase B** — Full onboarding, CDS account application, broker integration (pending Solomon Stockbrokers partnership)

---

## Status

Currently in pre-launch. Collecting waitlist signups ahead of broker partnership signing.

*Wekeza Tanzania. Popote ulipo.*