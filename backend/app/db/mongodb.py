from __future__ import annotations

from typing import Any

from pymongo import MongoClient

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class InMemoryStore:
    def __init__(self) -> None:
        self.influencers: dict[str, dict[str, Any]] = {}
        self.discovery_runs: dict[str, dict[str, Any]] = {}
        self.messages: dict[str, dict[str, Any]] = {}
        self.outreach_logs: dict[str, dict[str, Any]] = {}


memory_store = InMemoryStore()


def _build_client():
    if not settings.mongodb_uri:
        return None
    try:
        client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
        logger.info("MongoDB connected")
        return client
    except Exception as exc:  # pragma: no cover
        logger.warning("MongoDB unavailable: %s", exc)
        return None


client = _build_client()
database = client[settings.mongodb_database] if client else None


def get_database():
    return database


def check_database_connection() -> bool:
    return client is not None


def get_store():
    return database if database is not None else memory_store