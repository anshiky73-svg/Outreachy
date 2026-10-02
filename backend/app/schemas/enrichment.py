from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class EnrichmentRunRequest(BaseModel):
    influencerIds: list[str] | None = None
    maxPages: int = 3


class EnrichmentStatus(BaseModel):
    influencerId: str
    status: str
    emailFound: bool
    emailSource: Optional[str] = None
    notes: str
