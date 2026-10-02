from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.db.mongodb import get_store


class DiscoveryRepository:
    def __init__(self) -> None:
        self.store = get_store()

    def create(self, run: dict[str, Any]) -> dict[str, Any]:
        run_id = run.get("_id") or f"run-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        run["_id"] = run_id
        run.setdefault("startedAt", datetime.now(timezone.utc).isoformat())
        run.setdefault("status", "RUNNING")
        collection = self.store.discovery_runs if hasattr(self.store, "discovery_runs") else self.store["discovery_runs"]
        if isinstance(collection, dict):
            collection[run_id] = run
            return run
        collection.insert_one(run)
        return run

    def get(self, run_id: str) -> dict[str, Any] | None:
        collection = self.store.discovery_runs if hasattr(self.store, "discovery_runs") else self.store["discovery_runs"]
        if isinstance(collection, dict):
            return collection.get(run_id)
        return collection.find_one({"_id": run_id})

    def list(self) -> list[dict[str, Any]]:
        collection = self.store.discovery_runs if hasattr(self.store, "discovery_runs") else self.store["discovery_runs"]
        if isinstance(collection, dict):
            return list(collection.values())
        return list(collection.find().sort("startedAt", -1))

    def update(self, run_id: str, **updates: Any) -> dict[str, Any] | None:
        collection = self.store.discovery_runs if hasattr(self.store, "discovery_runs") else self.store["discovery_runs"]
        if isinstance(collection, dict):
            item = collection.get(run_id)
            if item is None:
                return None
            item.update(updates)
            collection[run_id] = item
            return item
        collection.update_one({"_id": run_id}, {"$set": updates})
        return collection.find_one({"_id": run_id})
