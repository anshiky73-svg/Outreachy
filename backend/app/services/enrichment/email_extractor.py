from __future__ import annotations

import re


class EmailExtractor:
    @staticmethod
    def extract(text: str) -> str:
        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text or "")
        return match.group(0) if match else "Not Found"
