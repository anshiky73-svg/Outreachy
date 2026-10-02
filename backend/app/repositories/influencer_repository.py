from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.db.mongodb import get_store


class InfluencerRepository:
    def __init__(self) -> None:
        self.store = get_store()

    def list(self, skip: int = 0, limit: int = 50, platform: str | None = None, niche: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        collection = self.store.influencers if hasattr(self.store, "influencers") else self.store["influencers"]
        items = list(collection.values()) if isinstance(collection, dict) else list(collection.find())
        if platform:
            items = [item for item in items if item.get("platform") == platform]
        if niche:
            items = [item for item in items if item.get("niche") == niche or niche.lower() in str(item.get("niche", "")).lower()]
        if status:
            items = [item for item in items if item.get("qualificationStatus") == status]
        return items[skip: skip + limit]

    def get(self, influencer_id: str) -> dict[str, Any] | None:
        collection = self.store.influencers if hasattr(self.store, "influencers") else self.store["influencers"]
        if isinstance(collection, dict):
            return collection.get(influencer_id)
        return collection.find_one({"_id": influencer_id})

    def upsert(self, influencer: dict[str, Any]) -> dict[str, Any]:
        influencer_id = influencer.get("_id") or influencer.get("id")
        if not influencer_id:
            influencer_id = f"inf-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
            influencer["_id"] = influencer_id
        if influencer.get("createdAt") is None:
            influencer["createdAt"] = datetime.now(timezone.utc).isoformat()
        influencer["updatedAt"] = datetime.now(timezone.utc).isoformat()

        collection = self.store.influencers if hasattr(self.store, "influencers") else self.store["influencers"]
        if isinstance(collection, dict):
            collection[influencer_id] = influencer
            return influencer
        collection.update_one({"_id": influencer_id}, {"$set": influencer}, upsert=True)
        return influencer

    def count(self) -> int:
        collection = self.store.influencers if hasattr(self.store, "influencers") else self.store["influencers"]
        if isinstance(collection, dict):
            return len(collection)
        return collection.count_documents({})

    def export_rows(self) -> list[dict[str, Any]]:
        return self.list(limit=5000)

    def delete_all(self) -> None:
        collection = self.store.influencers if hasattr(self.store, "influencers") else self.store["influencers"]
        if isinstance(collection, dict):
            collection.clear()
        else:
            collection.delete_many({})
