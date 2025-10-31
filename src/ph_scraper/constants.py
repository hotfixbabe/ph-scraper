BASE_URL = "https://www.pornhub.com"
DOMAIN = "pornhub.com"
DOMAIN_NAME = "pornhub"
VIDEO_URL_BASE = "https://www.pornhub.com/view_video.php?viewkey="
VALID_CONTENT_TYPE = {"channels", "model", "pornstar"}


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
