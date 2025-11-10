from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from ph_scraper.constants import BASE_URL, DOMAIN, DOMAIN_NAME, HOSTNAME
from ph_scraper.errors import URLError


@dataclass
class PornHubURL:
    url: str

    def __post_init__(self):
        self.base_url = BASE_URL
        self.domain = DOMAIN
        self.domain_name = DOMAIN_NAME
        self.hostname = HOSTNAME

        self.url = self.url.strip()
        self._parsed = urlparse(self.url)
        self._validate_domain(self._parsed.hostname)

        self.path = self._parsed.path or "/"
        self.path_parts = self.path.strip("/").split("/")
        self._rebuild_url()

    def _validate_domain(self, hostname: str | None) -> None:
        if not hostname.endswith(self.domain):
            raise URLError(f"Invalid domain: '{hostname}' (expected {self.hostname}).")

    def _rebuild_url(self) -> None:
        self.url = f"{self.base_url}{self.path}"
