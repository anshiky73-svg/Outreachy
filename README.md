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

- Backend: Python, FastAPI, Pydantic, PyMongo, httpx, BeautifulSoup
- Frontend: React, TypeScript, React Router, TanStack Query, Vite
- Storage: MongoDB-ready repository layer with graceful fallback behavior when no database is configured

## Local development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
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

## Workflow demonstrated

1. Discovery: search and collect creators by niche and platform relevance
2. Filtering: apply relevance, engagement, and quality thresholds
3. Enrichment: gather contact and profile signals
4. AI: generate personalized outreach copy
5. Sending: create outbound campaign messages and logs
6. Tracking: monitor statuses, opens, replies, and performance

## Environment configuration

Create a `.env` file in the backend root or use the values from your deployment environment for the following:

```env
APP_NAME="Influencer Outreach AI"
DEBUG=true
FRONTEND_URL=http://localhost:5173
MONGODB_URI=mongodb://localhost:27017
YOUTUBE_API_KEY=your_key_here
LLM_API_KEY=your_key_here
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_email
SMTP_PASSWORD=your_password
```

> If the database or external providers are not configured, the app keeps running in a graceful degraded mode for local prototyping and dashboard review.
