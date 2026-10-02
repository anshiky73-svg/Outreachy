from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.repositories.influencer_repository import InfluencerRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.outreach_repository import OutreachRepository
from app.services.outreach.duplicate_checker import DuplicateChecker
from app.services.outreach.email_service import EmailService


class OutreachService:
    def __init__(self) -> None:
        self.influencer_repository = InfluencerRepository()
        self.message_repository = MessageRepository()
        self.outreach_repository = OutreachRepository()
        self.email_service = EmailService()
        self.duplicate_checker = DuplicateChecker()

    def get_logs(self) -> list[dict[str, Any]]:
        return self.outreach_repository.list()

    def get_by_id(self, log_id: str) -> dict[str, Any] | None:
        return self.outreach_repository.get(log_id)

    def simulate_email(self, influencer_id: str) -> dict[str, Any]:
        influencer = self.influencer_repository.get(influencer_id)
        if influencer is None:
            raise KeyError("Influencer not found")
        message = self.message_repository.get_for_influencer(influencer_id)
        if message is None:
            raise ValueError("No message exists for this influencer")
        recipient = influencer.get("contactEmail") or "Not Found"
        if recipient == "Not Found":
            raise ValueError("No public email available")
        return self.email_service.simulate(influencer_id, message["_id"], recipient)

    def send_email(self, influencer_id: str) -> dict[str, Any]:
        influencer = self.influencer_repository.get(influencer_id)
        if influencer is None:
            raise KeyError("Influencer not found")
        message = self.message_repository.get_for_influencer(influencer_id)
        if message is None:
            raise ValueError("No message exists for this influencer")
        recipient = influencer.get("contactEmail") or "Not Found"
        if recipient == "Not Found":
            raise ValueError("No public email available")
        return self.email_service.send(influencer_id, message["_id"], recipient)

    def mark_dm_sent(self, influencer_id: str) -> dict[str, Any]:
        log = {
            "_id": f"log-{influencer_id}-dm",
            "influencerId": influencer_id,
            "channel": "instagram",
            "recipient": "@creator",
            "messageId": f"msg-{influencer_id}",
            "status": "MANUAL_SENT",
            "sentAt": datetime.now(timezone.utc).isoformat(),
            "failureReason": None,
            "attemptCount": 1,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat(),
        }
        return self.outreach_repository.create(log)
