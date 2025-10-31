from __future__ import annotations


class ScraperError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
