from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class OutreachSendRequest(BaseModel):
    channel: str = "email"


class OutreachRecord(BaseModel):
    influencerId: str
    channel: str
    recipient: str
    messageId: Optional[str] = None
    status: str = "READY"
    sentAt: Optional[str] = None
    failureReason: Optional[str] = None
    attemptCount: int = 0
