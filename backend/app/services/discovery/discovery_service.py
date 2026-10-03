from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.core.config import settings
from app.core.logging import get_logger
from app.repositories.discovery_repository import DiscoveryRepository
from app.repositories.influencer_repository import InfluencerRepository
from app.services.discovery.youtube_client import YouTubeClient

logger = get_logger(__name__)


class DiscoveryService:
    def __init__(self) -> None:
        self.youtube_client = YouTubeClient()
        self.discovery_repository = DiscoveryRepository()
        self.influencer_repository = InfluencerRepository()

    @staticmethod
    def _normalize_qualifier(raw_value: Any) -> int | None:
        if raw_value is None or raw_value == "Not Found":
            return None
        try:
            return int(raw_value)
        except (TypeError, ValueError):
            return None

    def _qualify_candidate(self, follower_count: int | None, themes: list[str], recent_content: list[str], description: str | None) -> tuple[str, list[str]]:
        reasons: list[str] = []

        if follower_count is None:
            reasons.append("Subscriber count unavailable.")
        elif settings.min_followers <= follower_count <= settings.max_followers:
            reasons.append("5K–100K subscriber range")
        else:
            reasons.append(f"Subscriber count {follower_count} is outside the 5K–100K micro-influencer range.")

        if themes:
            reasons.append("Technology niche detected")
        else:
            reasons.append("Technology niche not detected")

        if recent_content:
            reasons.append("Recent videos show technology-related content")
        else:
            reasons.append("Recent video context unavailable")

        if description and description != "Not Found":
            reasons.append("Sufficient public profile information")
        else:
            reasons.append("Limited public profile information")

        status = "QUALIFIED" if (
            follower_count is not None
            and settings.min_followers <= follower_count <= settings.max_followers
            and bool(themes)
            and bool(recent_content)
        ) else "FAILED"
        return status, reasons

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
            "developer productivity",
            "coding tutorials",
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

        seen: set[str] = set()
        channel_candidates: list[dict[str, Any]] = []
        try:
            for query in queries[: settings.scraper_max_queries]:
                search_results = await self.youtube_client.search_channels(query, max_results=settings.scraper_max_results_per_query)
                for item in search_results:
                    channel_url = item.get("channelUrl") or item.get("profileUrl")
                    dedupe_key = channel_url.split("?", 1)[0].rstrip("/") if channel_url else None
                    if not dedupe_key or dedupe_key in seen:
                        continue
                    seen.add(dedupe_key)
                    channel_candidates.append({"query": query, **item})
                    if len(channel_candidates) >= min(candidate_limit, settings.scraper_max_candidates):
                        break
                if len(channel_candidates) >= min(candidate_limit, settings.scraper_max_candidates):
                    break
        except ValueError as exc:
            run["status"] = "FAILED"
            run["error"] = str(exc)
            self.discovery_repository.update(run["_id"], **run)
            return run
        except Exception as exc:  # pragma: no cover
            logger.exception("Discovery query failed: %s", exc)
            run["status"] = "FAILED"
            run["error"] = str(exc)
            self.discovery_repository.update(run["_id"], **run)
            return run

        run["candidatesFound"] = len(channel_candidates)
        stored_count = 0
        qualified_count = 0
        for candidate in channel_candidates:
            channel_url = candidate.get("channelUrl") or candidate.get("profileUrl")
            if not channel_url:
                continue
            try:
                detail = await self.youtube_client.get_channel_details(channel_url)
            except Exception as exc:  # pragma: no cover
                logger.warning("Skipping YouTube channel %s due to scraper failure: %s", channel_url, exc)
                continue

            follower_count = self._normalize_qualifier(detail.get("followerCount") or candidate.get("subscriberCount"))
            description = detail.get("description") or candidate.get("description") or "Not Found"
            recent_content = detail.get("recentContent") or []
            themes = detail.get("contentThemes") or []
            status, reasons = self._qualify_candidate(follower_count, themes, recent_content, description)
            if status == "QUALIFIED":
                qualified_count += 1

            influencer = {
                "_id": f"youtube-{detail.get('platformId') or channel_url}",
                "platform": "youtube",
                "platformId": detail.get("platformId") or channel_url,
                "name": detail.get("name") or candidate.get("channelName") or "Not Found",
                "profileUrl": detail.get("profileUrl") or channel_url,
                "description": description,
                "followerCount": follower_count or 0,
                "engagementRate": detail.get("engagementRate"),
                "engagementRateType": detail.get("engagementRateType") or "estimated",
                "engagementCalculationMethod": detail.get("engagementCalculationMethod") or "Not Found",
                "niche": niche,
                "contentThemes": themes or ["Technology"],
                "contentStyle": detail.get("contentStyle") or "technology education and creator tutorials",
                "recentContent": recent_content,
                "contactEmail": detail.get("contactEmail") or "Not Found",
                "emailSource": detail.get("emailSource") or "not_found",
                "website": detail.get("website") or None,
                "instagramUrl": None,
                "youtubeUrl": detail.get("profileUrl") or channel_url,
                "tiktokUrl": None,
                "audienceAge": "Not Found",
                "audienceGender": "Not Found",
                "audienceGeography": "Not Found",
                "qualificationStatus": status,
                "qualificationScore": round(0.5 + (0.5 if status == "QUALIFIED" else 0.0), 2),
                "qualificationReasons": reasons,
                "brandFitScore": float(detail.get("contentRelevanceScore", 0.0) or 0.0),
                "contentRelevanceScore": float(detail.get("contentRelevanceScore", 0.0) or 0.0),
                "discoverySource": "youtube_public_scrape",
                "discoveryQuery": candidate.get("query") or " | ".join(queries),
                "discoveredAt": datetime.now(timezone.utc).isoformat(),
                "createdAt": datetime.now(timezone.utc).isoformat(),
                "updatedAt": datetime.now(timezone.utc).isoformat(),
            }
            self.influencer_repository.upsert(influencer)
            stored_count += 1

        run["storedCount"] = stored_count
        run["qualifiedCount"] = qualified_count
        run["failedCount"] = max(0, len(channel_candidates) - stored_count)
        run["status"] = "COMPLETED"
        run["completedAt"] = datetime.now(timezone.utc).isoformat()
        self.discovery_repository.update(run["_id"], **run)
        return run
