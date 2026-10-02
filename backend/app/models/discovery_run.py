from __future__ import annotations

from typing import Any


class DiscoveryRunRecord(dict):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        self.update(kwargs)
