from __future__ import annotations

from typing import Any


class ContentClassifier:
    @staticmethod
    def classify(influencer: dict[str, Any]) -> dict[str, Any]:
        text = " ".join(
            [
                str(influencer.get("description") or ""),
                " ".join(influencer.get("recentContent") or []),
                " ".join(influencer.get("contentThemes") or []),
            ]
        ).lower()

        if not text:
            return {"themes": ["technology"], "style": "unclassified", "contentRelevanceScore": 0.5}

        themes = []
        for theme in ["ai", "programming", "developer tools", "coding", "software reviews", "machine learning", "productivity", "web development"]:
            if theme in text:
                themes.append(theme)
        if not themes:
            themes = ["technology"]

        style = "practical and technical" if any(word in text for word in ["tutorial", "coding", "ai", "developer"]) else "general creator"
        relevance = min(0.96, 0.55 + (len(themes) * 0.08))
        return {"themes": themes, "style": style, "contentRelevanceScore": round(relevance, 2)}
