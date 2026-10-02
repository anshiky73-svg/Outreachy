from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import settings


class LLMClient:
    def __init__(self, provider: str | None = None, api_key: str | None = None, model: str | None = None) -> None:
        self.provider = provider or settings.llm_provider
        self.api_key = api_key or settings.llm_api_key
        self.model = model or settings.llm_model

    async def complete(self, prompt: str, temperature: float = 0.3) -> str:
        if not self.provider or not self.api_key:
            return self._local_fallback(prompt)

        if self.provider.lower() == "openai":
            payload = {
                "model": self.model,
                "temperature": temperature,
                "messages": [{"role": "user", "content": prompt}],
            }
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            async with httpx.AsyncClient(timeout=40) as client:
                response = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

        return self._local_fallback(prompt)

    def _local_fallback(self, prompt: str) -> str:
        if "email" in prompt.lower():
            return json.dumps({
                "emailSubject": "Technology Creator Collaboration",
                "emailBody": "Hi [creator], I loved how your recent technology content connects with developer workflows and emerging AI tools. Your focus on practical product education makes your audience highly relevant for a thoughtful collaboration. I would love to explore a sponsored product feature or creator-led review that gives your community a clear use-case and value. Let\'s discuss a tailored campaign that feels authentic and useful.",
                "instagramDm": "Your AI tooling breakdowns are genuinely useful—would love to explore a collaboration idea for your audience.",
                "personalizationSignals": ["technology-focused creator", "AI and developer tooling content", "highly relevant audience"],
            })
        return json.dumps({
            "emailSubject": "Technology Collaboration",
            "emailBody": "Hi [creator], I appreciated the way you explain technology products in a practical, accessible way. Your recent work speaks directly to developers and builders who value useful, well-explained guidance. I think a collaboration around a product feature, testimonial, or creator-led tutorial could be a strong fit for your audience. I would love to explore a tailored campaign that feels authentic and aligned with your content.",
            "instagramDm": "Your recent product breakdowns are a strong fit for a practical creator collaboration.",
            "personalizationSignals": ["technology creator", "developer-focused audience", "practical content style"],
        })
