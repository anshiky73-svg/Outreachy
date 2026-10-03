# AI-Powered Automated Micro-Influencer Outreach System

A full-stack monorepo that demonstrates the complete outreach workflow:

- Discovery of relevant micro-creators
- Filtering and qualification scoring
- Data enrichment for contact and profile context
- AI-powered personalization for email and DM outreach
- Sending simulation and tracking for response outcomes
- Dashboard monitoring across discovery, outreach, and message health

## Project structure

- backend/: FastAPI application and services
- frontend/: React + Vite dashboard for the outreach workflow

## Stack

- Backend: Python, FastAPI, Pydantic, PyMongo, Playwright, BeautifulSoup
- Frontend: React, TypeScript, React Router, TanStack Query, Vite
- Storage: MongoDB-ready repository layer with graceful fallback behavior when no database is configured

## Local development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m playwright install chromium
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Default app routes

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Health check: http://localhost:8000/api/health

## YouTube discovery workflow

This project replaces the YouTube Data API with a public Playwright scraper that reads public YouTube search and channel pages without requiring a Google Cloud project, API key, OAuth flow, or login.

1. Discovery: scrape public YouTube search pages for tech-focused creators
2. Filtering: keep micro-influencers in the 5K–100K range when public data is visible
3. Enrichment: inspect channel/about pages for recent content, website links, and public email addresses
4. AI: generate personalized outreach copy using public profile signals
5. Sending: continue in simulation mode unless the user intentionally triggers a send
6. Tracking: monitor responses and outreach logs in the dashboard

## Environment configuration

Create a `.env` file in the backend root or use the values from your deployment environment for the following:

```env
APP_NAME="Influencer Outreach AI"
DEBUG=true
FRONTEND_URL=http://localhost:5173
MONGODB_URI=mongodb://localhost:27017
LLM_API_KEY=your_key_here
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_email
SMTP_PASSWORD=your_password
SCRAPER_HEADLESS=true
SCRAPER_TIMEOUT_MS=30000
SCRAPER_DELAY_MIN_MS=1000
SCRAPER_DELAY_MAX_MS=2500
SCRAPER_MAX_CANDIDATES=150
SCRAPER_MAX_QUERIES=10
SCRAPER_MAX_RESULTS_PER_QUERY=15
```

> The app does not require `YOUTUBE_API_KEY`. Discovery uses public YouTube pages only.

## Limitations

- YouTube's public page structure can change and break selectors occasionally.
- Some subscriber counts are hidden on YouTube and remain unavailable.
- Some engagement metrics are not public and may be missing.
- Not every creator publishes a public email address.
- Email addresses are only extracted when explicitly published; they are never guessed.
- Instagram DM remains a manual or simulated workflow.
- The scraper uses public information only and does not log in or bypass CAPTCHA or access controls.

> If the database or external providers are not configured, the app keeps running in a graceful degraded mode for local prototyping and dashboard review.
