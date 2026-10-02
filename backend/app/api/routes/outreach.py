from __future__ import annotations

import csv
import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.repositories.outreach_repository import OutreachRepository
from app.services.outreach.outreach_service import OutreachService

router = APIRouter(prefix="/api", tags=["Outreach"])


@router.post("/outreach/send/{influencer_id}")
def send_email(influencer_id: str):
    try:
        return OutreachService().send_email(influencer_id)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/outreach/simulate/{influencer_id}")
def simulate_email(influencer_id: str):
    try:
        return OutreachService().simulate_email(influencer_id)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/outreach/mark-dm-sent/{influencer_id}")
def mark_dm_sent(influencer_id: str):
    return OutreachService().mark_dm_sent(influencer_id)


@router.get("/outreach/logs")
def list_outreach_logs():
    return OutreachService().get_logs()


@router.get("/outreach/{log_id}")
def get_outreach_log(log_id: str):
    record = OutreachService().get_by_id(log_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Outreach log not found")
    return record


@router.get("/outreach/export")
def export_outreach_logs():
    rows = OutreachRepository().list()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Influencer", "Email", "Subject", "Email Body", "Instagram DM", "Status"])
    for row in rows:
        writer.writerow([
            row.get("influencerId", "N/A"),
            row.get("recipient", "N/A"),
            row.get("messageId", "N/A"),
            row.get("status", "N/A"),
            row.get("channel", "N/A"),
            row.get("status", "N/A"),
        ])
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=outreach_messages.csv"})
