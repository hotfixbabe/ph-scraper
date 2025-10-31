from ph_scraper import ProfileScraper


def main():
    try:
        urls = [
            "https://www.pornhub.com/channels/nubilefilms",
            "https://www.pornhub.com/model/sweetie-fox",
            "https://www.pornhub.com/pornstar/riley-reid",
        ]
        for u in urls:
            with ProfileScraper(u) as scraper:
                vs = scraper.get_pub_videos()
                print(u)
                print(f"pub_videos: {len(vs)}")

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
