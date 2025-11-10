# Domain constants
BASE_URL = "https://www.pornhub.com"
DOMAIN = "pornhub.com"
DOMAIN_NAME = "pornhub"
HOSTNAME = "www.pornhub.com"
VIDEO_URL_BASE = "https://www.pornhub.com/view_video.php?viewkey="

# Session
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Content
KEY_PUB_VIDEOS = "pub_videos"
PROFILE_CONTENT_TYPES = {"channels", "model", "pornstar"}
PROFILE_CONTENT_MAP = {
    "channels": {
        KEY_PUB_VIDEOS: {
            "path": "/videos",
            "selectors": {
                "ul_id": "showAllChanelVideos",
            },
        },
    },
    "model": {
        KEY_PUB_VIDEOS: {
            "path": "/videos",
            "selectors": {
                "ul_id": "mostRecentVideosSection",
            },
        },
    },
    "pornstar": {
        KEY_PUB_VIDEOS: {
            "path": "/videos/upload",
            "selectors": {
                "ul_id": "moreData",
            },
        },
    },
}
