# Domain constants
BASE_URL = "https://www.pornhub.com"
DOMAIN = "pornhub.com"
DOMAIN_NAME = "pornhub"
VIDEO_URL_BASE = "https://www.pornhub.com/view_video.php?viewkey="


# Content
CONTENT_MAP = {
    "channels": {
        "public_uploaded_videos": {
            "path": "/videos",
            "selectors": {
                "ul_id": "showAllChanelVideos",
            },
        },
    },
    "model": {
        "public_uploaded_videos": {
            "path": "/videos",
            "selectors": {
                "ul_id": "mostRecentVideosSection",
            },
        },
    },
    "pornstar": {
        "public_uploaded_videos": {
            "path": "/videos/upload",
            "selectors": {
                "ul_id": "moreData",
            },
        },
    },
}
KEY_PUB_VIDEOS = "public_uploaded_videos"
VALID_CONTENT_TYPE = {"channels", "model", "pornstar"}


# Session
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
