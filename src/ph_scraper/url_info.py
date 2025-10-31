from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class URLInfo:
    content_type: str
    profile_name: str
    profile_url: str

    def to_dict(self) -> dict:
        return asdict(self)
