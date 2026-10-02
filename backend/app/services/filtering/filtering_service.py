from __future__ import annotations

from typing import Any

from app.core.config import settings
from app.repositories.influencer_repository import InfluencerRepository


class FilteringService:
    def __init__(self) -> None:
        self.influencer_repository = InfluencerRepository()

    def evaluate_influencer(self, influencer: dict[str, Any]) -> dict[str, Any]:
        reasons: list[str] = []
        follower_count = int(influencer.get("followerCount") or 0)
        engagement_rate = float(influencer.get("engagementRate") or 0.0)
        niche = str(influencer.get("niche") or "")
        content_relevance = float(influencer.get("contentRelevanceScore") or 0.0)
        brand_fit = float(influencer.get("brandFitScore") or 0.0)

        if follower_count < settings.min_followers:
            reasons.append(f"Follower count {follower_count} is below minimum {settings.min_followers}.")
        if follower_count > settings.max_followers:
            reasons.append(f"Follower count {follower_count} exceeds maximum {settings.max_followers}.")
        if not niche or "tech" not in niche.lower() and "technology" not in niche.lower() and "ai" not in niche.lower() and "program" not in niche.lower() and "software" not in niche.lower() and "developer" not in niche.lower():
            reasons.append("Technology niche not detected.")
        if engagement_rate < settings.min_engagement_rate:
            reasons.append(f"Estimated engagement rate {engagement_rate:.2f}% is below minimum {settings.min_engagement_rate:.2f}%.")
        if content_relevance < settings.min_content_relevance:
            reasons.append(f"Content relevance {content_relevance:.2f} is below threshold {settings.min_content_relevance:.2f}.")
        if brand_fit < settings.min_brand_fit:
            reasons.append(f"Brand fit {brand_fit:.2f} is below threshold {settings.min_brand_fit:.2f}.")

        score = 0.0
        if settings.min_followers <= follower_count <= settings.max_followers:
            score += 20
        if engagement_rate >= settings.min_engagement_rate:
            score += 25
        if niche and any(term in niche.lower() for term in ["tech", "technology", "ai", "programming", "software", "developer"]):
            score += 25
        if content_relevance >= settings.min_content_relevance:
            score += 20
        if brand_fit >= settings.min_brand_fit:
            score += 10

        status = "QUALIFIED" if not reasons else "FAILED"
        result = {
            "influencerId": influencer.get("_id") or influencer.get("platformId"),
            "qualificationStatus": status,
            "qualificationReasons": reasons,
            "qualificationScore": round(score, 2),
        }
        influencer["qualificationStatus"] = status
        influencer["qualificationReasons"] = reasons
        influencer["qualificationScore"] = round(score, 2)
        self.influencer_repository.upsert(influencer)
        return result

    def run(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        influencers = self.influencer_repository.list(limit=5000)
        for influencer in influencers:
            results.append(self.evaluate_influencer(influencer))
        return results
