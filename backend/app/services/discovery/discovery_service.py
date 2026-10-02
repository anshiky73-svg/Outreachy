from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.core.config import settings
from app.core.exceptions import ExternalServiceError
from app.repositories.discovery_repository import DiscoveryRepository
from app.repositories.influencer_repository import InfluencerRepository
from app.services.discovery.youtube_client import YouTubeClient


class DiscoveryService:
    def __init__(self) -> None:
        self.youtube_client = YouTubeClient()
        self.discovery_repository = DiscoveryRepository()
        self.influencer_repository = InfluencerRepository()

    async def run(self, niche: str = "Technology", queries: list[str] | None = None, candidate_limit: int = 150) -> dict[str, Any]:
        queries = queries or [
            "AI tools",
            "artificial intelligence",
            "programming",
            "software development",
            "coding",
            "web development",
            "machine learning",
            "developer tools",
            "tech reviews",
            "software engineering",
        ]
        run = {
            "_id": f"run-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            "niche": niche,
            "queries": queries,
            "candidatesFound": 0,
            "duplicatesFound": 0,
            "storedCount": 0,
            "qualifiedCount": 0,
            "failedCount": 0,
            "status": "RUNNING",
            "startedAt": datetime.now(timezone.utc).isoformat(),
            "completedAt": None,
            "error": None,
        }
        self.discovery_repository.create(run)

        if not settings.youtube_api_key:
            run["status"] = "COMPLETED"
            run["completedAt"] = datetime.now(timezone.utc).isoformat()
            run["error"] = "YouTube API key is not configured. Discovery cannot run until YOUTUBE_API_KEY is set."
            self.discovery_repository.update(run["_id"], **run)
            return run

        seen: set[str] = set()
        channel_candidates: list[dict[str, Any]] = []
        try:
            for query in queries:
                search_results = await self.youtube_client.search_channels(query, max_results=15)
                for item in search_results:
                    channel_id = item.get("snippet", {}).get("channelId") or item.get("id", {}).get("channelId")
                    if not channel_id or channel_id in seen:
                        continue
                    seen.add(channel_id)
                    channel_candidates.append(item)
                    if len(channel_candidates) >= candidate_limit:
                        break
                if len(channel_candidates) >= candidate_limit:
                    break
        except Exception as exc:  # pragma: no cover
            run["status"] = "FAILED"
            run["error"] = str(exc)
            self.discovery_repository.update(run["_id"], **run)
            return run

        run["candidatesFound"] = len(channel_candidates)
        channel_ids = [item.get("snippet", {}).get("channelId") or item.get("id", {}).get("channelId") for item in channel_candidates if item.get("snippet", {}).get("channelId") or item.get("id", {}).get("channelId")]

        try:
            channel_details = await self.youtube_client.get_channels(channel_ids)
        except ExternalServiceError as exc:
            run["status"] = "FAILED"
            run["error"] = str(exc)
            self.discovery_repository.update(run["_id"], **run)
            return run

        for detail in channel_details:
            channel_id = detail.get("id")
            if not channel_id:
                continue
            stats = detail.get("statistics", {}) or {}
            snippet = detail.get("snippet", {}) or {}
            profile_url = f"https://www.youtube.com/channel/{channel_id}"
            subscriber_count = int(stats.get("subscriberCount", 0) or 0)
            influencer = {
                "_id": f"youtube-{channel_id}",
                "platform": "youtube",
                "platformId": channel_id,
                "name": snippet.get("title") or "Not Found",
                "profileUrl": profile_url,
                "description": snippet.get("description") or "Not Found",
                "followerCount": subscriber_count,
                "engagementRate": 0.0,
                "engagementRateType": "estimated",
                "engagementCalculationMethod": "(likes + comments) / views * 100 across recent videos",
                "niche": niche,
                "contentThemes": ["technology"],
                "contentStyle": "creator content",
                "recentContent": [],
                "contactEmail": "Not Found",
                "emailSource": "not_found",
                "website": None,
                "instagramUrl": None,
                "youtubeUrl": profile_url,
                "tiktokUrl": None,
                "audienceAge": "Not Found",
                "audienceGender": "Not Found",
                "audienceGeography": "Not Found",
                "qualificationStatus": "PENDING",
                "qualificationScore": 0.0,
                "qualificationReasons": [],
                "brandFitScore": 0.0,
                "contentRelevanceScore": 0.0,
                "discoverySource": "youtube",
                "discoveryQuery": " | ".join(queries),
                "discoveredAt": datetime.now(timezone.utc).isoformat(),
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat(),
            }
            self.influencer_repository.upsert(influencer)

        run["storedCount"] = len(channel_details)
        run["status"] = "COMPLETED"
        run["completedAt"] = datetime.now(timezone.utc).isoformat()
        self.discovery_repository.update(run["_id"], **run)
        return run
