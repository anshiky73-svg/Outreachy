from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings
from app.core.exceptions import ExternalServiceError


class YouTubeClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.youtube_api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    async def search_channels(self, query: str, max_results: int = 15) -> list[dict[str, Any]]:
        if not self.api_key:
            raise ExternalServiceError("YouTube API key is not configured.")
        params = {
            "part": "snippet",
            "q": query,
            "type": "channel",
            "maxResults": max_results,
            "key": self.api_key,
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            payload = response.json()
        return payload.get("items", [])

    async def get_channels(self, channel_ids: list[str]) -> list[dict[str, Any]]:
        if not self.api_key:
            raise ExternalServiceError("YouTube API key is not configured.")
        if not channel_ids:
            return []
        params = {
            "part": "snippet,statistics,brandingSettings,status",
            "id": ",".join(channel_ids),
            "key": self.api_key,
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(f"{self.base_url}/channels", params=params)
            response.raise_for_status()
            payload = response.json()
        return payload.get("items", [])

    async def get_recent_videos(self, channel_id: str, max_results: int = 10) -> list[dict[str, Any]]:
        if not self.api_key:
            raise ExternalServiceError("YouTube API key is not configured.")
        params = {
            "part": "snippet,id",
            "channelId": channel_id,
            "type": "video",
            "maxResults": max_results,
            "order": "date",
            "key": self.api_key,
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            payload = response.json()
        return payload.get("items", [])

    async def get_video_statistics(self, video_ids: list[str]) -> dict[str, dict[str, Any]]:
        if not self.api_key:
            raise ExternalServiceError("YouTube API key is not configured.")
        if not video_ids:
            return {}
        params = {
            "part": "statistics,snippet",
            "id": ",".join(video_ids),
            "key": self.api_key,
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(f"{self.base_url}/videos", params=params)
            response.raise_for_status()
            payload = response.json()
        result: dict[str, dict[str, Any]] = {}
        for item in payload.get("items", []):
            result[item.get("id")] = item.get("statistics", {})
        return result
