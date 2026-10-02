from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class FilteringConfig(BaseModel):
    minFollowers: int = 5000
    maxFollowers: int = 100000
    minEngagementRate: float = 1.5
    minContentRelevance: float = 0.55
    minBrandFit: float = 0.5
    niche: str = "Technology"


class QualificationResult(BaseModel):
    influencerId: str
    qualificationStatus: str
    qualificationReasons: list[str] = Field(default_factory=list)
    qualificationScore: float = 0.0



class FilteringSummary(BaseModel):
    total: int
    qualified: int
    failed: int
    results: list[QualificationResult]
