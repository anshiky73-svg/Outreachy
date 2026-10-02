from __future__ import annotations

import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from typing import Any

from app.core.config import settings
from app.core.exceptions import DuplicateOutreachError, ValidationError
from app.repositories.message_repository import MessageRepository
from app.repositories.outreach_repository import OutreachRepository


class EmailService:
    def __init__(self) -> None:
        self.message_repository = MessageRepository()
        self.outreach_repository = OutreachRepository()

    def validate_recipient(self, email: str) -> str:
        if not email or email == "Not Found":
            raise ValidationError("No public email available for this influencer.")
        return email

    def simulate(self, influencer_id: str, message_id: str, recipient: str) -> dict[str, Any]:
        if self.outreach_repository.has_duplicate(influencer_id, "email"):
            raise DuplicateOutreachError("A prior outreach record already exists for this influencer on email.")
        record = {
            "_id": f"log-{influencer_id}-email",
            "influencerId": influencer_id,
            "channel": "email",
            "recipient": recipient,
            "messageId": message_id,
            "status": "SIMULATED",
            "sentAt": datetime.now(timezone.utc).isoformat(),
            "failureReason": None,
            "attemptCount": 1,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat(),
        }
        return self.outreach_repository.create(record)

    def send(self, influencer_id: str, message_id: str, recipient: str) -> dict[str, Any]:
        if self.outreach_repository.has_duplicate(influencer_id, "email"):
            raise DuplicateOutreachError("A prior outreach record already exists for this influencer on email.")
        if settings.email_mode != "smtp" or not settings.smtp_host or not settings.smtp_from_email:
            return self.simulate(influencer_id, message_id, recipient)

        try:
            message = EmailMessage()
            message["Subject"] = self.message_repository.get(message_id).get("emailSubject", "Collaboration")
            message["From"] = settings.smtp_from_email
            message["To"] = recipient
            message.set_content(self.message_repository.get(message_id).get("emailBody", ""))
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
                if settings.smtp_username:
                    smtp.login(settings.smtp_username, settings.smtp_password)
                smtp.send_message(message)
        except Exception as exc:
            record = {
                "_id": f"log-{influencer_id}-email",
                "influencerId": influencer_id,
                "channel": "email",
                "recipient": recipient,
                "messageId": message_id,
                "status": "FAILED",
                "sentAt": None,
                "failureReason": str(exc),
                "attemptCount": 1,
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat(),
            }
            return self.outreach_repository.create(record)

        record = {
            "_id": f"log-{influencer_id}-email",
            "influencerId": influencer_id,
            "channel": "email",
            "recipient": recipient,
            "messageId": message_id,
            "status": "SENT",
            "sentAt": datetime.now(timezone.utc).isoformat(),
            "failureReason": None,
            "attemptCount": 1,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat(),
        }
        return self.outreach_repository.create(record)
