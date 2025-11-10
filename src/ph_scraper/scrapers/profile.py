from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypeVar

from ph_scraper.constants import KEY_PUB_VIDEOS, PROFILE_CONTENT_MAP
from ph_scraper.media.video import Video
from ph_scraper.urls.profile import ProfileURL

from .scraper import PornHubScraper

T = TypeVar("T")


@dataclass()
class ProfileScraper(PornHubScraper):
    def __post_init__(self):
        super().__post_init__()
        self._profile_url = ProfileURL(self.url)
        self.content_type = self._profile_url.content_type
        self.url = self._profile_url.url

    def get_url_info(self) -> ProfileURL:
        """Returns parsed profile URL information."""
        return self._profile_url

    def get_pub_videos(self) -> list[Video]:
        """Returns public videos from the profile."""
        return self._extract_videos(KEY_PUB_VIDEOS)

    def _extract_videos(self, key: str) -> list[Video]:
        type_config = PROFILE_CONTENT_MAP[self.content_type].get(key)
        url = f"{self.url}{type_config['path']}"
        selectors = type_config["selectors"]

        all_videos: list[dict] = []
        new_videos: list[dict] = []
        cached: list[dict] = self.cache_data.get(key) or []
        index = {v["vkey"]: v for v in cached if v.get("vkey")}

        page = 1

        while True:
            response = self._fetch(url, page=page)
            if response.status_code == 404:
                break

            html = response.text
            if not html:
                break

            extracted = self._extract_videos_from_html(html, selectors)
            fresh = [v for v in extracted if v["vkey"] not in index]

            if not fresh:
                break

            new_videos.extend(fresh)
            for v in fresh:
                index[v["vkey"]] = v

            page += 1

        if new_videos:
            new_videos.extend(cached)
            all_videos = new_videos
            self.cache_data[key] = all_videos
            self._cache_save()
        else:
            all_videos = cached

        return [Video(**v) for v in all_videos]


def with_profile_scraper(
    method_name: str,
    *,
    method_kwargs: dict[str, Any] | None = None,
    **scraper_kwargs: Any,
) -> T:
    """
    Calls a method on ProfileScraper.

    Parameters
    ----------
    method_name : str
        The method name to call.
    method_kwargs : dict
        Arguments to pass to the method.
    **scraper_kwargs
        Other constructor arguments for ProfileScraper
        (e.g., url, retries, timeout, session, etc.)
    """

    method_kwargs = method_kwargs or {}

    with ProfileScraper(**scraper_kwargs) as scraper:
        method = getattr(scraper, method_name)
        return method(**method_kwargs)


def get_profile_url_info(url: str, **scraper_kwargs: Any) -> ProfileURL:
    """See ProfileScraper.get_url_info"""
    return with_profile_scraper("get_url_info", url=url, **scraper_kwargs)


def get_profile_pub_videos(url: str, **scraper_kwargs: Any) -> list[Video]:
    """See ProfileScraper.get_pub_videos"""
    return with_profile_scraper("get_pub_videos", url=url, **scraper_kwargs)
