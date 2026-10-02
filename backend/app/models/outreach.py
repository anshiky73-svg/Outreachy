from __future__ import annotations

from typing import Any


class OutreachLogRecord(dict):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__()
        self.update(kwargs)
