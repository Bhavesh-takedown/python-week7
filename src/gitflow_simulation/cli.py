"""Command line entry point for the release-notes helper."""

import argparse
import sys

from gitflow_simulation.release_notes import build_release_notes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Group Conventional Commit messages into release notes."
    )
    parser.add_argument("--tag", required=True, help="release tag, such as v1.2.0")
    parser.add_argument(
        "commits",
        nargs="+",
        help='commit messages, for example "feat: add search"',
    )
    args = parser.parse_args()

    try:
        print(build_release_notes(args.tag, args.commits))
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    sys.exit(main())
