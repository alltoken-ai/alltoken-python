"""AllToken API error type."""
from __future__ import annotations


class AllTokenError(Exception):
    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(f"AllToken API error {status_code}: {body}")
