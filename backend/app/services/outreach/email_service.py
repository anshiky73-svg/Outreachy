from __future__ import annotations

import logging
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from typing import Any

from app.core.config import settings
from app.core.exceptions import DuplicateOutreachError, ValidationError
from app.repositories.message_repository import MessageRepository
from app.repositories.outreach_repository import OutreachRepository

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self) -> None:
        self.message_repository = MessageRepository()
        self.outreach_repository = OutreachRepository()

    def validate_recipient(self, email: str) -> str:
        if not email or email == "Not Found":
            raise ValidationError("No public email available for this influencer.")
        return email

    def is_smtp_configured(self) -> bool:
        return bool(
            settings.smtp_host
            and settings.smtp_port
            and settings.smtp_username
            and settings.smtp_password
            and settings.smtp_from_email
        )

    def _send_via_smtp(self, message: EmailMessage) -> None:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as smtp:
            smtp.ehlo()
            if settings.smtp_use_tls:
                smtp.starttls()
                smtp.ehlo()
            if settings.smtp_username and settings.smtp_password:
                smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(message)

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
        if settings.email_mode != "smtp" or not self.is_smtp_configured():
            return self.simulate(influencer_id, message_id, recipient)

        try:
            message = EmailMessage()
            message["Subject"] = self.message_repository.get(message_id).get("emailSubject", "Collaboration")
            message["From"] = settings.smtp_from_email
            message["To"] = recipient
            message.set_content(self.message_repository.get(message_id).get("emailBody", ""))
            self._send_via_smtp(message)
        except smtplib.SMTPAuthenticationError:
            logger.exception("SMTP authentication failed for Gmail SMTP")
            failure_reason = "SMTP authentication failed. Check the Gmail address and App Password."
        except (smtplib.SMTPException, OSError):
            logger.exception("SMTP send failed for outreach email")
            failure_reason = "SMTP sending failed. Verify the Gmail host, port, and STARTTLS configuration."
        else:
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

        record = {
            "_id": f"log-{influencer_id}-email",
            "influencerId": influencer_id,
            "channel": "email",
            "recipient": recipient,
            "messageId": message_id,
            "status": "FAILED",
            "sentAt": None,
            "failureReason": failure_reason,
            "attemptCount": 1,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat(),
        }
        return self.outreach_repository.create(record)

    def send_test_email(self, recipient: str) -> dict[str, Any]:
        recipient = self.validate_recipient(recipient)
        if not self.is_smtp_configured():
            raise ValidationError("SMTP is not configured. Set the Gmail host, port, username, password, and sender email.")

        message = EmailMessage()
        message["Subject"] = "SMTP Configuration Test"
        message["From"] = settings.smtp_from_email
        message["To"] = recipient
        message.set_content("This is a test email from the Automated Micro-Influencer Outreach System.")

        try:
            self._send_via_smtp(message)
        except smtplib.SMTPAuthenticationError:
            logger.exception("SMTP authentication failed during test email")
            return {
                "status": "failed",
                "recipient": recipient,
                "error": "SMTP authentication failed. Check the Gmail address and App Password.",
            }
        except (smtplib.SMTPException, OSError):
            logger.exception("SMTP testing failed")
            return {
                "status": "failed",
                "recipient": recipient,
                "error": "SMTP test failed. Verify the Gmail host, port, and STARTTLS configuration.",
            }

        return {
            "status": "sent",
            "recipient": recipient,
            "subject": "SMTP Configuration Test",
        }
