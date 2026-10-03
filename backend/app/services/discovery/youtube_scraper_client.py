from __future__ import annotations

import asyncio
import random
import re
from typing import Any
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from app.core.config import settings
from app.core.logging import get_logger
from app.services.enrichment.email_extractor import EmailExtractor

logger = get_logger(__name__)


class YouTubeScraperClient:
    def __init__(self) -> None:
        self.headless = settings.scraper_headless
        self.timeout_ms = settings.scraper_timeout_ms
        self.delay_min_ms = settings.scraper_delay_min_ms
        self.delay_max_ms = settings.scraper_delay_max_ms
        self.max_channels_per_query = settings.scraper_max_results_per_query
        self.max_queries = settings.scraper_max_queries
        self.max_candidates = settings.scraper_max_candidates
        self._playwright = None
        self._browser = None

    async def _ensure_browser(self):
        if self._browser is None:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=self.headless)
        return self._browser

    async def close(self) -> None:
        if self._browser is not None:
            await self._browser.close()
            self._browser = None
        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None

    async def _delay(self) -> None:
        if self.delay_min_ms <= 0 and self.delay_max_ms <= 0:
            return
        delay = random.uniform(self.delay_min_ms / 1000.0, self.delay_max_ms / 1000.0)
        await asyncio.sleep(delay)

    async def _new_page(self, url: str, wait_for_selector: str | None = None):
        browser = await self._ensure_browser()
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1440, "height": 1400},
            locale="en-US",
            java_script_enabled=True,
        )
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            if wait_for_selector:
                await page.wait_for_selector(wait_for_selector, timeout=max(5000, self.timeout_ms // 2), state="visible")
        except Exception as exc:  # pragma: no cover - graceful failure path
            logger.warning("Page partially loaded for %s: %s", url, exc)
        return page, context

    @staticmethod
    def _normalize_youtube_url(raw_url: str | None) -> str | None:
        if not raw_url:
            return None
        url = raw_url.strip()
        if not url:
            return None
        if url.startswith("//"):
            url = f"https:{url}"
        if url.startswith("/"):
            url = f"https://www.youtube.com{url}"
        if "youtube.com" not in url and "youtu.be" not in url:
            return None
        return url.split("?", 1)[0].split("#", 1)[0]

    @staticmethod
    def _coerce_text(value: Any) -> str:
        if value is None:
            return "Not Found"
        text = str(value).strip().replace("\xa0", " ")
        return text or "Not Found"

    @staticmethod
    def _extract_channel_id(url: str | None) -> str | None:
        if not url:
            return None
        match = re.search(r"/channel/([^/?#]+)", url)
        if match:
            return match.group(1)
        match = re.search(r"/@([^/?#]+)", url)
        if match:
            return f"@{match.group(1)}"
        return None

    @staticmethod
    def _extract_subscriber_count(raw_value: str | None) -> int | None:
        if not raw_value or raw_value == "Not Found":
            return None
        text = re.sub(r"\s+", " ", str(raw_value)).strip()
        match = re.search(r"([\d,]+(?:\.\d+)?[KMB]?)\s*(?:subscribers|subscriber)", text, re.IGNORECASE)
        if not match:
            return None
        value = match.group(1).replace(",", "")
        if value.endswith("K"):
            multiplier = 1000
            numeric = float(value[:-1])
        elif value.endswith("M"):
            multiplier = 1000000
            numeric = float(value[:-1])
        elif value.endswith("B"):
            multiplier = 1000000000
            numeric = float(value[:-1])
        else:
            multiplier = 1
            numeric = float(value)
        return int(numeric * multiplier)

    @staticmethod
    def _extract_email_candidates(text: str | None) -> list[str]:
        if not text:
            return []
        return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

    @staticmethod
    def _pick_theme_hits(text: str | None) -> list[str]:
        if not text:
            return []
        haystack = text.lower()
        theme_map = {
            "AI": ["ai", "artificial intelligence", "machine learning", "llm"],
            "Machine Learning": ["machine learning", "ml", "deep learning"],
            "Programming": ["programming", "code", "coding", "software engineering"],
            "Web Development": ["web development", "frontend", "backend", "javascript", "react", "html", "css"],
            "Software Engineering": ["software engineering", "dev tools", "developer tools", "software development"],
            "Developer Tools": ["developer tools", "productivity", "tooling", "workflow"],
            "Tech Reviews": ["tech reviews", "review", "gadget", "product review"],
            "Technology": ["technology", "tech", "startup"],
        }
        hits: list[str] = []
        for label, terms in theme_map.items():
            if any(term in haystack for term in terms):
                hits.append(label)
        return hits

    @staticmethod
    def _to_about_url(channel_url: str) -> str:
        normalized = channel_url.rstrip("/")
        if "/channel/" in normalized:
            return f"{normalized}/about"
        if normalized.startswith("https://www.youtube.com/@"):
            return f"{normalized}/about"
        return normalized

    @staticmethod
    def _extract_video_links(page) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        try:
            videos = page.locator("a#video-title").all()
            for video in videos[:10]:
                href = video.get_attribute("href")
                title = (video.inner_text() or "").strip()
                if not href or not title:
                    continue
                if "/watch?v=" not in href:
                    continue
                results.append({
                    "title": title,
                    "url": f"https://www.youtube.com{href.split('&', 1)[0]}",
                    "views": "Not Found",
                    "likes": "Not Found",
                    "comments": "Not Found",
                    "publishedAt": "Not Found",
                })
        except Exception:
            return []
        return results

    async def search_channels(self, query: str, max_results: int = 15) -> list[dict[str, Any]]:
        encoded_query = quote_plus(query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        page, context = await self._new_page(url, "ytd-channel-renderer")
        results: list[dict[str, Any]] = []
        try:
            renderers = page.locator("ytd-channel-renderer")
            count = min(await renderers.count(), max(max_results * 2, max_results))
            for index in range(count):
                renderer = renderers.nth(index)
                href = None
                for selector in ("a[href*='/channel/']", "a[href*='/@']", "a#channel-name"):
                    candidate = renderer.locator(selector).first
                    href = await candidate.get_attribute("href")
                    if href:
                        break
                if not href:
                    continue
                normalized_url = self._normalize_youtube_url(href)
                if not normalized_url:
                    continue
                channel_name = await self._safe_text(renderer.locator("#channel-name, a#channel-name, yt-formatted-string").first())
                description = await self._safe_text(renderer.locator("#description-text, .description, yt-formatted-string").first())
                subscriber_text = await self._safe_text(renderer.locator("#subscriber-count, .subscriber-count").first())
                subscriber_count = self._extract_subscriber_count(subscriber_text)
                results.append({
                    "channelName": self._coerce_text(channel_name),
                    "channelUrl": normalized_url,
                    "profileUrl": normalized_url,
                    "description": self._coerce_text(description),
                    "subscriberCount": subscriber_count,
                    "query": query,
                })
                if len(results) >= max_results:
                    break
        except Exception as exc:  # pragma: no cover
            logger.warning("Unable to extract YouTube search results for %s: %s", query, exc)
            raise ValueError("Unable to extract YouTube search results. YouTube page structure may have changed.") from exc
        finally:
            await context.close()
        return results

    async def get_channel_details(self, channel_url: str) -> dict[str, Any]:
        normalized_url = self._normalize_youtube_url(channel_url)
        if not normalized_url:
            raise ValueError("Invalid YouTube channel URL.")
        about_url = self._to_about_url(normalized_url)
        page, context = await self._new_page(normalized_url, "#channel-name")
        try:
            channel_name = await self._safe_text(page.locator("#channel-name, meta[itemprop='name']").first())
            description = await self._safe_text(page.locator("#description, #description-container, meta[name='description']").first())
            subscriber_text = await self._safe_text(page.locator("#subscriber-count, yt-formatted-string#subscriber-count").first())
            subscriber_count = self._extract_subscriber_count(subscriber_text)
            channel_id = self._extract_channel_id(normalized_url)
            about_page, about_context = await self._new_page(about_url, "#channel-handle")
            try:
                website_candidates = []
                for selector in ("#link-list a[href]", "a[href*='http']", "#channel-handle + a[href]"):
                    links = about_page.locator(selector)
                    for index in range(min(await links.count(), 20)):
                        href = await links.nth(index).get_attribute("href")
                        if href and href.startswith(("http://", "https://")):
                            website_candidates.append(href)
                website = None
                for candidate in website_candidates:
                    if "youtube.com" not in candidate and "google.com" not in candidate:
                        website = candidate
                        break
                website_text = await self._safe_text(about_page.locator("body"))
                email_candidates = self._extract_email_candidates(website_text)
                lead_email = email_candidates[0] if email_candidates else EmailExtractor.extract(description or "")
                email_source = "public_profile" if lead_email and lead_email != "Not Found" else "Not Found"
            finally:
                await about_context.close()

            recent_videos = self._extract_video_links(page)
            if not recent_videos:
                videos_page, videos_context = await self._new_page(f"{normalized_url.rstrip('/')}/videos", "a#video-title")
                try:
                    recent_videos = self._extract_video_links(videos_page)
                finally:
                    await videos_context.close()

            content_bundle = " ".join([description or "", *[video.get("title", "") for video in recent_videos]])
            theme_hits = self._pick_theme_hits(content_bundle)
            content_relevance = round(min(1.0, max(0.0, len(theme_hits) / 5.0)), 2)

            result = {
                "platform": "youtube",
                "platformId": channel_id or normalized_url,
                "name": self._coerce_text(channel_name),
                "profileUrl": normalized_url,
                "channelUrl": normalized_url,
                "description": self._coerce_text(description),
                "followerCount": subscriber_count,
                "subscriberCount": subscriber_count,
                "website": website,
                "contactEmail": lead_email if lead_email and lead_email != "Not Found" else "Not Found",
                "emailSource": email_source,
                "recentContent": [video.get("title") for video in recent_videos],
                "recentVideos": recent_videos,
                "contentThemes": theme_hits or ["Technology"],
                "contentStyle": "technology education and creator tutorials",
                "niche": "Technology",
                "engagementRate": None,
                "engagementRateType": "estimated",
                "engagementCalculationMethod": "Not Found",
                "qualificationStatus": "PENDING",
                "qualificationReasons": [],
                "brandFitScore": 0.0,
                "contentRelevanceScore": content_relevance,
                "discoverySource": "youtube_public_scrape",
                "query": "Technology",
            }
            return result
        finally:
            await context.close()

    async def _safe_text(self, locator) -> str:
        try:
            if locator is None:
                return "Not Found"
            count = await locator.count()
            for index in range(min(count, 5)):
                value = await locator.nth(index).inner_text()
                if value and value.strip():
                    return value.strip()
            return "Not Found"
        except Exception:
            return "Not Found"
