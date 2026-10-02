from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.discovery import router as discovery_router
from app.api.routes.enrichment import router as enrichment_router
from app.api.routes.filtering import router as filtering_router
from app.api.routes.health import router as health_router
from app.api.routes.influencers import router as influencers_router
from app.api.routes.messages import router as messages_router
from app.api.routes.outreach import router as outreach_router
from app.api.routes.personalization import router as personalization_router
from app.api.routes.pipeline import router as pipeline_router
from app.api.routes.settings import router as settings_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-powered influencer outreach workflow for discovery, filtering, enrichment, and outreach tracking.",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(dashboard_router)
app.include_router(discovery_router)
app.include_router(influencers_router)
app.include_router(filtering_router)
app.include_router(enrichment_router)
app.include_router(personalization_router)
app.include_router(outreach_router)
app.include_router(messages_router)
app.include_router(pipeline_router)
app.include_router(settings_router)


@app.get("/")
def root():
    return {"message": "Influencer Outreach AI API", "status": "running"}


@app.get("/api")
def api_root():
    return {"message": "Influencer Outreach AI API", "status": "running", "version": "1.0.0"}