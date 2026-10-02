from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.db.mongodb import get_store


class OutreachRepository:
    def __init__(self) -> None:
        self.store = get_store()

    def list(self) -> list[dict[str, Any]]:
        collection = self.store.outreach_logs if hasattr(self.store, "outreach_logs") else self.store["outreach_logs"]
        if isinstance(collection, dict):
            return list(collection.values())
        return list(collection.find().sort("createdAt", -1))

    def create(self, item: dict[str, Any]) -> dict[str, Any]:
        record_id = item.get("_id") or item.get("id") or f"out-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        item["_id"] = record_id
        item.setdefault("createdAt", datetime.now(timezone.utc).isoformat())
        item["updatedAt"] = datetime.now(timezone.utc).isoformat()
        collection = self.store.outreach_logs if hasattr(self.store, "outreach_logs") else self.store["outreach_logs"]
        if isinstance(collection, dict):
            collection[record_id] = item
            return item
        collection.insert_one(item)
        return item

    def get(self, log_id: str) -> dict[str, Any] | None:
        collection = self.store.outreach_logs if hasattr(self.store, "outreach_logs") else self.store["outreach_logs"]
        if isinstance(collection, dict):
            return collection.get(log_id)
        return collection.find_one({"_id": log_id})

    def has_duplicate(self, influencer_id: str, channel: str) -> bool:
        collection = self.store.outreach_logs if hasattr(self.store, "outreach_logs") else self.store["outreach_logs"]
        if isinstance(collection, dict):
            for item in collection.values():
                if item.get("influencerId") == influencer_id and item.get("channel") == channel:
                    return True
            return False
        return collection.find_one({"influencerId": influencer_id, "channel": channel}) is not None
