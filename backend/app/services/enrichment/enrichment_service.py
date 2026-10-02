from __future__ import annotations

from app.repositories.influencer_repository import InfluencerRepository
from app.services.enrichment.email_extractor import EmailExtractor
from app.services.enrichment.website_scraper import WebsiteScraper


class EnrichmentService:
    def __init__(self) -> None:
        self.repository = InfluencerRepository()
        self.scraper = WebsiteScraper()

    async def enrich_influencer(self, influencer_id: str) -> dict[str, str | bool | None]:
        influencer = self.repository.get(influencer_id)
        if influencer is None:
            raise KeyError("Influencer not found")

        candidates = [
            influencer.get("website"),
            influencer.get("profileUrl"),
            influencer.get("instagramUrl"),
        ]
        email = "Not Found"
        source = "not_found"
        notes = "No public contact email found."

        for candidate in candidates:
            if not candidate:
                continue
            page = await self.scraper.fetch(candidate)
            found_email = EmailExtractor.extract(page.get("content") or "")
            if found_email != "Not Found":
                email = found_email
                source = "creator_website" if "http" in str(candidate) else "public_profile"
                notes = f"Found public email on {candidate}."
                break

        description = str(influencer.get("description") or "")
        description_email = EmailExtractor.extract(description)
        if description_email != "Not Found":
            email = description_email
            source = "youtube_description"
            notes = "Found public contact email in channel description."

        influencer["contactEmail"] = email
        influencer["emailSource"] = source
        self.repository.upsert(influencer)
        return {"influencerId": influencer_id, "status": "completed", "emailFound": email != "Not Found", "emailSource": source, "notes": notes}

    async def run(self, influencer_ids: list[str] | None = None) -> list[dict[str, str | bool | None]]:
        items = self.repository.list(limit=5000)
        selected = [item for item in items if not influencer_ids or item.get("_id") in influencer_ids]
        result = []
        for item in selected:
            result.append(await self.enrich_influencer(item.get("_id")))
        return result
