from __future__ import annotations

from dataclasses import dataclass

from ph_scraper.constants import PROFILE_CONTENT_TYPES
from ph_scraper.errors import URLError

from .base import PornHubURL


@dataclass
class ProfileURL(PornHubURL):
    def __post_init__(self):
        super().__post_init__()
        self.content_type: str | None = None
        self.profile_name: str | None = None
        self._parse_profile_path()
        self.url = f"{self.base_url}/{self.content_type}/{self.profile_name}"

    def _parse_profile_path(self) -> None:
        if len(self.path_parts) < 2:
            raise URLError("Invalid profile URL structure.")

        content_type = self.path_parts[0]
        profile_name = self.path_parts[1]

        if content_type not in PROFILE_CONTENT_TYPES:
            raise URLError(f"Unsupported content type: '{content_type}'.")
        if not profile_name:
            raise URLError("Profile name is empty.")

        self.content_type = content_type
        self.profile_name = profile_name
