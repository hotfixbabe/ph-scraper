import argparse

from .__version__ import __description__, __title__, __version__


def parse_args():
    parser = argparse.ArgumentParser(
        description=(f"{__description__}\n\n"),
        formatter_class=argparse.RawTextHelpFormatter,
        prog=__title__,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{__title__} {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # profile
    profile = subparsers.add_parser("profile")
    profile.add_argument("url")
    profile.add_argument("-c", "--cache", type=str)

    # profile group 01
    profile_g1 = profile.add_mutually_exclusive_group(required=True)
    profile_g1.add_argument("--get-pub-videos", action="store_true")

    # profile group 02
    profile_g2 = profile.add_mutually_exclusive_group()
    profile_g2.add_argument("-j", "--print-json", action="store_true")
    profile_g2.add_argument("-u", "--print-url", action="store_true")
    profile_g2.set_defaults(print_url=True)

    return parser.parse_args()
