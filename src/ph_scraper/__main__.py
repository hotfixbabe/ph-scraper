from pathlib import Path

from ph_scraper import Video, get_profile_pub_videos
from ph_scraper.args_parser import parse_args
from ph_scraper.utils.json import dump_json


def print_videos(output_format: str, vids: list[Video]) -> None:
    if output_format == "json":
        print(dump_json([v.to_dict() for v in vids]))
    elif output_format == "url":
        print("\n".join(v.url for v in vids))


def main():
    try:
        args = parse_args()

        if args.command == "profile":
            if args.get_pub_videos:
                cache_path = Path(args.cache) if getattr(args, "cache", None) else None
                vids = get_profile_pub_videos(args.url, cache_path=cache_path)
                print_videos(args.output_format, vids)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
