from __future__ import annotations

from pydantic import BaseModel, Field


class PersonalizationInput(BaseModel):
    influencerId: str


class PersonalizationOutput(BaseModel):
    emailSubject: str
    emailBody: str
    instagramDm: str
    personalizationSignals: list[str] = Field(default_factory=list)


class MessageRecordCreate(BaseModel):
    influencerId: str
    emailSubject: str
    emailBody: str
    instagramDm: str
    personalizationSignals: list[str] = Field(default_factory=list)
    model: str = "local"
    promptVersion: str = "v1"
    status: str = "READY"
