from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class DiscoveryRunCreate(BaseModel):
    niche: str = "Technology"
    queries: list[str] = Field(default_factory=list)
    candidateLimit: int = 150


class DiscoveryRunResponse(BaseModel):
    id: str
    niche: str
    queries: list[str]
    candidatesFound: int = 0
    duplicatesFound: int = 0
    storedCount: int = 0
    qualifiedCount: int = 0
    failedCount: int = 0
    status: str = "RUNNING"
    startedAt: Optional[str] = None
    completedAt: Optional[str] = None
    error: Optional[str] = None


class DiscoveryRunResults(BaseModel):
    runId: str
    influencers: list[dict[str, Any]]
