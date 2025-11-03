from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requests import RequestException, Response, Session

from .constants import (
    BASE_URL,
    CONTENT_MAP,
    DEFAULT_HEADERS,
    DOMAIN,
    KEY_PUB_VIDEOS,
    VALID_CONTENT_TYPE,
)
from .errors import ScraperError
from .url_info import URLInfo
from .utils.json import read_json, write_json
from .video import Video

T = TypeVar("T")


@dataclass()
class ProfileScraper:
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
        self.url_info = self._parse_url()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
        return False

    def get_url_info(self) -> URLInfo:
        return self.url_info

    def get_pub_videos(self) -> list[Video]:
        return self._extract_videos(KEY_PUB_VIDEOS)

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

    def _extract_videos(self, key: str) -> list[Video]:
        def _extract_html(html: str, selectors: dict) -> list[dict[str, str]]:
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

        type_config = CONTENT_MAP[self.url_info.content_type].get(key)
        url = f"{self.url_info.profile_url}{type_config['path']}"
        selectors = type_config["selectors"]
        all_videos: list[dict] = []
        new_videos: list[dict] = []
        cached: list[dict] = self.cache_data.get(key) or []
        cached_index = {v["vkey"]: v for v in cached if v.get("vkey")}
        page = 1

        while True:
            response = self._fetch(url, page=page)
            if response.status_code == 404:
                break

            html = response.text
            if not html:
                break

            extracted = _extract_html(html, selectors)
            fresh = [v for v in extracted if v["vkey"] not in cached_index]

            if not fresh:
                break

            new_videos.extend(fresh)
            for v in fresh:
                cached_index[v["vkey"]] = v

            page += 1

        if new_videos:
            new_videos.extend(cached)
            all_videos = new_videos
            self.cache_data[key] = all_videos
            self._cache_save()
        else:
            all_videos = cached

        return [Video(**v) for v in all_videos]

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

    def _parse_url(self) -> URLInfo:
        response = self._fetch(self.url)
        if response.status_code == 404:
            raise ScraperError("Profile page not found.")

        url = response.url
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        path = parsed.path.strip("/").split("/")
        content_type = path[0] if len(path) > 0 else ""
        profile_name = path[1] if len(path) > 1 else ""

        if not hostname.endswith(DOMAIN):
            raise ScraperError(f"Domain is not {DOMAIN}.")
        if content_type not in VALID_CONTENT_TYPE:
            raise ScraperError(f"Unsupported content_type: '{content_type}'.")
        if not profile_name:
            raise ScraperError("Profile name is empty.")

        return URLInfo(
            content_type=content_type,
            profile_name=profile_name,
            profile_url=f"{BASE_URL}/{content_type}/{profile_name}",
        )


def with_profile_scraper(
    method_name: str,
    *,
    method_kwargs: dict[str, Any] | None = None,
    **scraper_kwargs: Any,
) -> T:
    """
    Calls a method on ProfileScraper.

    Parameters:
        method_name: str - the method name to call.
        method_kwargs: dict - arguments to pass to the method.
        **scraper_kwargs: other constructor arguments for ProfileScraper
            (url, retries, timeout, session, etc.)
    """
    method_kwargs = method_kwargs or {}

    with ProfileScraper(**scraper_kwargs) as scraper:
        method = getattr(scraper, method_name)
        return method(**method_kwargs)


def get_profile_url_info(url: str) -> URLInfo:
    return with_profile_scraper("get_url_info", url=url)


def get_profile_pub_videos(url: str, **scraper_kwargs: Any) -> list[Video]:
    return with_profile_scraper("get_pub_videos", url=url, **scraper_kwargs)
