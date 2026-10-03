from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import settings
from app.core.exceptions import ValidationError
from app.db.mongodb import check_database_connection
from app.services.outreach.email_service import EmailService

router = APIRouter(prefix="/api", tags=["Settings"])


class EmailTestRequest(BaseModel):
    recipient: str


@router.get("/settings")
def system_settings():
    scraper_ready = settings.scraper_timeout_ms > 0 and settings.scraper_max_candidates > 0
    return {
        "database": "Configured" if check_database_connection() else "Not configured",
        "youtubeApi": "Ready" if scraper_ready else "Not configured",
        "llm": "Configured" if settings.llm_api_key else "Not configured",
        "smtp": "Configured" if settings.is_smtp_configured else "Not configured",
        "emailMode": settings.email_mode,
    }


@router.post("/settings/email/test")
def test_email_settings(payload: EmailTestRequest):
    try:
        return EmailService().send_test_email(payload.recipient)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="SMTP test failed. Check the Gmail configuration.",
        ) from exc
