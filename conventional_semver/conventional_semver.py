import argparse
import textwrap
import sys

from loguru import logger

from calculate import calculate_bump, calculate_new_version
from validate import parse


def _parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
            Calculate Semantic Versions using Conventional Commit messages!

            This CLI tool takes various inputs and calculates "the next SemVer"
            using the latest provided version and a commit message.
            In order to give the user maximum flexibility, it is possible to
            use the --latest-version and --commit-message arguments.
            This means you can use this CLI tool alongside any existing tooling
            that you might already be using.

            The tool provides the following functionality:

            (0) Use the manually provided version )--latest-version)
            (1) Look at the latest git tag to determine the latest version (--local)

            The parsing settings for the tool are provided under the [pccc] section
            in the pyproject.toml.
        """
        ),
    )

    parser.add_argument(
        "--verbose",
        "--debug",
        action="store_true",
        help="Set log level to DEBUG",
    )

    parser.add_argument(
        "-m",
        "--message",
        required=True,
        help="Text to be parsed as a Conventional Commit message",
    )

    parser.add_argument(
        "--pre-release",
        help="Add the specified text as a pre-release identifier (don't include leading -)",
    )

    parser.add_argument(
        "--build-meta",
        help="Add the specified text as a build-metadata identifier (don't include leading +)",
    )

    # It is possible to acquire the latest version as a manual input XOR from the git tag
    version_mutex = parser.add_mutually_exclusive_group()
    version_mutex.add_argument(
        "-v",
        "--latest-version",
        help="The latest version (on which the next SemVer will be based)",
    )

    version_mutex.add_argument(
        "-l",
        "--local",
        action="store_true",
        help="Determine the latest version using the latest available git-tag",
    )

    return parser.parse_args()


def main():
    """The general flow of the main program is as follows:

    (1) The commit message is parsed using PCCC.
    (2) The bump is determined based on the Conventional Commit type.
    (3) The current SemVer is determined using the chosen method.
    (4) The new SemVer is calculated.
    (5) The new SemVer is printed to stdout.
    """
    args = _parse_args()

    logger.remove()
    if args.verbose:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")

    logger.debug(f"Message:\n{args.message}")

    # Parse the commit message and compute the bump
    parsed_message = parse(args.message)
    bump = calculate_bump(parsed_message)

    # Determine how to get ahold of the latest version
    latest_version = None
    if args.latest_version:
        logger.debug(
            f"Latest Semantic Version was provided as an argument: {args.latest_version}"
        )
        latest_version = args.latest_version
    elif args.local:
        logger.debug(
            "Latest Semantic Version will be fetched from the current git branch"
        )
        logger.error("This functionality is not yet implemented!")
        raise

    new_version = calculate_new_version(
        latest_version, bump, args.pre_release, args.build_meta
    )

    logger.info(f"New version: {new_version}")
    return new_version


if __name__ == "__main__":
    print(main())
