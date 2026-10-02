from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.db.mongodb import get_store


class MessageRepository:
    def __init__(self) -> None:
        self.store = get_store()

    def create(self, item: dict[str, Any]) -> dict[str, Any]:
        message_id = item.get("_id") or item.get("id") or f"msg-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        item["_id"] = message_id
        item.setdefault("createdAt", datetime.now(timezone.utc).isoformat())
        item["updatedAt"] = datetime.now(timezone.utc).isoformat()
        collection = self.store.messages if hasattr(self.store, "messages") else self.store["messages"]
        if isinstance(collection, dict):
            collection[message_id] = item
            return item
        collection.insert_one(item)
        return item

    def get(self, message_id: str) -> dict[str, Any] | None:
        collection = self.store.messages if hasattr(self.store, "messages") else self.store["messages"]
        if isinstance(collection, dict):
            return collection.get(message_id)
        return collection.find_one({"_id": message_id})

    def list(self) -> list[dict[str, Any]]:
        collection = self.store.messages if hasattr(self.store, "messages") else self.store["messages"]
        if isinstance(collection, dict):
            return list(collection.values())
        return list(collection.find().sort("createdAt", -1))

    def get_for_influencer(self, influencer_id: str) -> dict[str, Any] | None:
        collection = self.store.messages if hasattr(self.store, "messages") else self.store["messages"]
        if isinstance(collection, dict):
            for item in collection.values():
                if item.get("influencerId") == influencer_id:
                    return item
            return None
        return collection.find_one({"influencerId": influencer_id})
