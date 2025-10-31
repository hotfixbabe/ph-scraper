from pathlib import Path

from ph_scraper import ProfileScraper, Video

from .args_parser import parse_args
from .utils.json import dump_json


def profile_scraper(
    url: str,
    cache_path: Path | None = None,
    method_name: str = "get_profile_data",
    *args,
    **kwargs,
):
    with ProfileScraper(url, cache_path=cache_path) as scraper:
        method = getattr(scraper, method_name)
        return method(*args, **kwargs)


def print_video(args, vs: list[Video]) -> None:
    if getattr(args, "print_json", False):
        print(dump_json([v.to_dict() for v in vs]))
    elif getattr(args, "print_url", False):
        print("\n".join(v.url for v in vs))


def main():
    try:
        args = parse_args()

        if args.command == "profile":
            if args.get_pub_videos:
                cache_path = Path(args.cache) if getattr(args, "cache", None) else None
                pub_videos = profile_scraper(
                    args.url, cache_path=cache_path, method_name="get_pub_videos"
                )
                print_video(args, pub_videos)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
