from __future__ import annotations

from dataclasses import asdict, dataclass

from ph_scraper.constants import VIDEO_URL_BASE


@dataclass(frozen=True)
class Video:
    vkey: str
    title: str | None = None
    duration: str | None = None
    thumb_url: str | None = None
    uploader: str | None = None
    views: str | None = None
    rating: str | None = None

    @property
    def url(self) -> str:
        return f"{VIDEO_URL_BASE}{self.vkey}"

    def to_dict(self) -> dict:
        return asdict(self)
