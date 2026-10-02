from __future__ import annotations

import csv
import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.repositories.message_repository import MessageRepository

router = APIRouter(prefix="/api", tags=["Messages"])


@router.get("/messages")
def list_messages():
    return MessageRepository().list()


@router.get("/messages/{message_id}")
def get_message(message_id: str):
    message = MessageRepository().get(message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.get("/messages/export")
def export_messages():
    rows = MessageRepository().list()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Influencer", "Email", "Subject", "Email Body", "Instagram DM", "Status"])
    for item in rows:
        writer.writerow([
            item.get("influencerId", "N/A"),
            item.get("emailSubject", "N/A"),
            item.get("emailBody", "N/A"),
            item.get("instagramDm", "N/A"),
            item.get("status", "N/A"),
        ])
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=messages.csv"})
