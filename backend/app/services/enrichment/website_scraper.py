from __future__ import annotations

import re
from typing import Any

import httpx


class WebsiteScraper:
    def __init__(self, timeout: float = 15.0) -> None:
        self.timeout = timeout

    async def fetch(self, url: str) -> dict[str, Any]:
        if not url or not url.startswith(("http://", "https://")):
            return {"url": url, "content": "", "emails": [], "urls": []}
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.get(url)
                response.raise_for_status()
                text = response.text or ""
        except Exception:
            return {"url": url, "content": "", "emails": [], "urls": []}

        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        urls = re.findall(r"https?://[^\s\"'<>]+", text)
        return {"url": url, "content": text[:5000], "emails": emails[:10], "urls": urls[:30]}
