from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings
from app.db.mongodb import check_database_connection

router = APIRouter(prefix="/api", tags=["Settings"])


@router.get("/settings")
def system_settings():
    return {
        "database": "Configured" if check_database_connection() else "Not configured",
        "youtubeApi": "Configured" if settings.youtube_api_key else "Not configured",
        "llm": "Configured" if settings.llm_api_key else "Not configured",
        "smtp": "Configured" if settings.smtp_host and settings.smtp_from_email else "Not configured",
        "emailMode": settings.email_mode,
    }
