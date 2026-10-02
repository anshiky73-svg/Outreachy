from __future__ import annotations

from app.repositories.outreach_repository import OutreachRepository


class DuplicateChecker:
    def __init__(self) -> None:
        self.repository = OutreachRepository()

    def is_duplicate(self, influencer_id: str, channel: str) -> bool:
        return self.repository.has_duplicate(influencer_id, channel)
