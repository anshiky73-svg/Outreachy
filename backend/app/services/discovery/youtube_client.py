from __future__ import annotations

from app.services.discovery.youtube_scraper_client import YouTubeScraperClient


class YouTubeClient(YouTubeScraperClient):
    """Backward-compatible YouTube client that uses the public Playwright scraper."""

    pass
