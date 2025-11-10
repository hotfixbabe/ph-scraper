from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup
from requests import RequestException, Response, Session

from ph_scraper.constants import DEFAULT_HEADERS
from ph_scraper.utils.json import read_json, write_json


@dataclass()
class PornHubScraper:
    """
    Scraper for profile pages.

    Attributes
    ----------
    url : str
        The profile URL to scrape.
    retries : int, optional
        Number of retries for HTTP requests. Default is 10.
    timeout : int, optional
        Timeout for HTTP requests in seconds. Default is 5.
    new_cache : bool, optional
        Whether to ignore existing cache. Default is False.
    cache_path : Path | None, optional
        Path to cache file. Default is None.
    session : Session | None, optional
        Requests Session to use. Default is None.
    """

    url: str
    retries: int = 10
    timeout: int = 5
    new_cache: bool = False
    cache_path: Path | None = None
    session: Session | None = None

    def __post_init__(self):
        if not self.session:
            self.session = Session()
            self.session.headers.update(DEFAULT_HEADERS)

        self.cache_data = self._cache_load()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
        return False

    def _cache_load(self) -> dict[str, list[str]]:
        if self.cache_path is None:
            return {}

        if self.new_cache:
            return {}

        return read_json(self.cache_path) or {}

    def _cache_save(self) -> None:
        if self.cache_path is None:
            return

        write_json(self.cache_path, self.cache_data)

    def _extract_videos_from_html(
        self, html: str, selectors: dict
    ) -> list[dict[str, str]]:
        results = []
        soup = BeautifulSoup(html, "html.parser")
        ul = soup.find("ul", id=selectors["ul_id"])
        if not ul:
            return results

        for i in ul.find_all("li"):
            vkey = i.get("data-video-vkey")
            if not vkey:
                continue

            title_elem = i.select_one(".thumbnailTitle")
            duration_elem = i.select_one(".duration")
            thumb_elem = i.select_one("img.js-videoThumb")
            uploader_elem = i.select_one(".usernameWrap a")
            views_elem = i.select_one(".views var")
            rating_elem = i.select_one(".rating-container .value")

            video = {
                "vkey": vkey,
                "title": title_elem.text.strip() if title_elem else None,
                "duration": duration_elem.text.strip() if duration_elem else None,
                "thumb_url": thumb_elem.get("src") if thumb_elem else None,
                "uploader": uploader_elem.text.strip() if uploader_elem else None,
                "views": views_elem.text.strip() if views_elem else None,
                "rating": rating_elem.text.strip() if rating_elem else None,
            }
            results.append(video)
        return results

    def _fetch(self, base_url: str, page: int = 1) -> Response:
        url = f"{base_url}?page={page}" if page > 1 else base_url
        for attempt in range(1, self.retries + 1):
            try:
                response = self.session.get(url, timeout=self.timeout)
                if response.status_code == 404:
                    return response
                response.raise_for_status()
                return response
            except RequestException:
                if attempt < self.retries:
                    continue
                raise
