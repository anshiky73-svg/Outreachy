from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class InfluencerBase(BaseModel):
    platform: str
    platformId: str
    name: str
    profileUrl: Optional[str] = None
    description: Optional[str] = None
    followerCount: int = 0
    engagementRate: Optional[float] = None
    engagementRateType: str = "estimated"
    engagementCalculationMethod: Optional[str] = None
    niche: Optional[str] = None
    contentThemes: list[str] = Field(default_factory=list)
    contentStyle: Optional[str] = None
    recentContent: list[str] = Field(default_factory=list)
    contactEmail: str = "Not Found"
    emailSource: str = "not_found"
    website: Optional[str] = None
    instagramUrl: Optional[str] = None
    youtubeUrl: Optional[str] = None
    tiktokUrl: Optional[str] = None
    audienceAge: Optional[str] = None
    audienceGender: Optional[str] = None
    audienceGeography: Optional[str] = None
    qualificationStatus: str = "PENDING"
    qualificationScore: float = 0.0
    qualificationReasons: list[str] = Field(default_factory=list)
    brandFitScore: float = 0.0
    contentRelevanceScore: float = 0.0
    discoverySource: Optional[str] = None
    discoveryQuery: Optional[str] = None
    discoveredAt: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class InfluencerCreate(InfluencerBase):
    pass


class InfluencerUpdate(BaseModel):
    platform: Optional[str] = None
    platformId: Optional[str] = None
    name: Optional[str] = None
    profileUrl: Optional[str] = None
    description: Optional[str] = None
    followerCount: Optional[int] = None
    engagementRate: Optional[float] = None
    engagementRateType: Optional[str] = None
    engagementCalculationMethod: Optional[str] = None
    niche: Optional[str] = None
    contentThemes: Optional[list[str]] = None
    contentStyle: Optional[str] = None
    recentContent: Optional[list[str]] = None
    contactEmail: Optional[str] = None
    emailSource: Optional[str] = None
    website: Optional[str] = None
    instagramUrl: Optional[str] = None
    youtubeUrl: Optional[str] = None
    tiktokUrl: Optional[str] = None
    audienceAge: Optional[str] = None
    audienceGender: Optional[str] = None
    audienceGeography: Optional[str] = None
    qualificationStatus: Optional[str] = None
    qualificationScore: Optional[float] = None
    qualificationReasons: Optional[list[str]] = None
    brandFitScore: Optional[float] = None
    contentRelevanceScore: Optional[float] = None
    discoverySource: Optional[str] = None
    discoveryQuery: Optional[str] = None
    discoveredAt: Optional[str] = None
    updatedAt: Optional[str] = None


class InfluencerResponse(InfluencerBase):
    id: str
    _id: str = ""
