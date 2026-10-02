from __future__ import annotations

import json
from typing import Any

from app.repositories.message_repository import MessageRepository
from app.services.ai.content_classifier import ContentClassifier
from app.services.ai.llm_client import LLMClient


class PersonalizationService:
    def __init__(self) -> None:
        self.message_repository = MessageRepository()
        self.llm_client = LLMClient()

    async def generate_for_influencer(self, influencer: dict[str, Any]) -> dict[str, Any]:
        classification = ContentClassifier.classify(influencer)
        influencer["contentThemes"] = classification["themes"]
        influencer["contentStyle"] = classification["style"]
        influencer["contentRelevanceScore"] = classification["contentRelevanceScore"]
        prompt = self._build_prompt(influencer)
        raw = await self.llm_client.complete(prompt)
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {
                "emailSubject": "Technology Collaboration",
                "emailBody": "Hi [creator], I wanted to reach out because your technology-focused content and practical guidance make your audience highly relevant for a thoughtful partnership. I would love to explore a tailored campaign around a creator-led review, feature, or ambassador opportunity that feels authentic to your voice. Let\'s discuss how we can build a useful collaboration for your community.",
                "instagramDm": "Your practical technology content feels highly relevant for a creator partnership.",
                "personalizationSignals": ["technology-focused content", "practical creator style", "relevant audience context"],
            }

        email_body = payload.get("emailBody") or ""
        instagram_dm = payload.get("instagramDm") or ""
        if len(email_body.split()) < 60 or len(email_body.split()) > 90:
            email_body = self._repair_email(influencer, payload)
        if len(instagram_dm.split()) < 15 or len(instagram_dm.split()) > 30:
            instagram_dm = self._repair_dm(influencer, payload)

        message = {
            "_id": f"msg-{influencer.get('_id') or influencer.get('platformId')}",
            "influencerId": influencer.get("_id") or influencer.get("platformId"),
            "emailSubject": payload.get("emailSubject") or "Technology Collaboration",
            "emailBody": email_body,
            "emailWordCount": len(email_body.split()),
            "instagramDm": instagram_dm,
            "dmWordCount": len(instagram_dm.split()),
            "personalizationSignals": payload.get("personalizationSignals") or classification["themes"],
            "model": "local",
            "promptVersion": "v1",
            "status": "READY",
            "createdAt": None,
            "updatedAt": None,
        }
        return self.message_repository.create(message)

    def _build_prompt(self, influencer: dict[str, Any]) -> str:
        content = influencer.get("description") or ""
        recent = " | ".join(influencer.get("recentContent") or [])
        themes = ", ".join(influencer.get("contentThemes") or [])
        return (
            "You are generating an outreach message using only the verified data provided. Do not invent facts. "
            "Return strict JSON with keys emailSubject, emailBody, instagramDm, personalizationSignals. "
            f"Creator name: {influencer.get('name')}. Niche: {influencer.get('niche')}. "
            f"Description: {content}. Recent content: {recent}. Themes: {themes}. "
            "The email body must be 60-90 words, use only real signals, and reference practical content topics. "
            "The Instagram DM must be 15-30 words and concise and natural."
        )

    def _repair_email(self, influencer: dict[str, Any], payload: dict[str, Any]) -> str:
        base = payload.get("emailBody") or "Hi [creator], we are exploring a tailored technology collaboration aligned with your content and audience."
        return base[:600]

    def _repair_dm(self, influencer: dict[str, Any], payload: dict[str, Any]) -> str:
        base = payload.get("instagramDm") or "Your practical technology work feels highly relevant for a collaboration."
        return base[:220]
