import argparse
from pathlib import Path
import textwrap
import sys

from git import Repo
from loguru import logger
from pyparsing.exceptions import ParseException

from conventional_semver.calculate import calculate_bump, calculate_new_version
from conventional_semver.validate import parse


def _parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
            Calculate Semantic Versions using Conventional Commit messages!

            The most basic usage of this tool is to create a configuration file
            (script expects it to be called config.toml, but you can use the
            --config argument to pass an arbitrary file) and pass a conventional
            commit message as input to the script.

            $> conventional_semver "fix: ensure /api/list-all returns properly"
            $> 0.0.1

            It is also possible to provide a SemVer as an argument and have the
            script calculate the next version:

            $> conventional_semver --semver 1.0.8 "feat: add new cool feature"
            $> 1.1.0

            The tool also supports the SemVer options for pre-releases and build metadata:

            --pre-release
            --build-meta

            which will append the provided strings in a SemVer compatible manner.

            $> conventional_semver --semver 1.0.8 --pre-release alpha.1 --build-meta $(date -I) "feat: add new cool feature"
            $> 1.1.0-alpha.1+2024-01-10

            Note that the lib used for SemVer parsing is a bit more relaxed than the
            official documentation, w.r.t. pre-release and build metadata.
            Make sure the strings provided follow the SemVer specification!
        """
        ),
    )

    # You cannot use --silent and --verbose at the same time...
    logging_mutex = parser.add_mutually_exclusive_group()
    logging_mutex.add_argument(
        "--silent",
        "-s",
        action="store_true",
        help="Disable logging",
    )

    logging_mutex.add_argument(
        "--verbose",
        "--debug",
        action="store_true",
        help="Set log level to DEBUG",
    )

    parser.add_argument(
        "--config",
        default="config.toml",
        help="Provide path to PCCC config file",
    )

    # It is possible to acquire the latest version as a manual input XOR from the git tag
    version_mutex = parser.add_mutually_exclusive_group()
    version_mutex.add_argument(
        "--semver",
        help="The latest Semantic Version (on which the next SemVer will be based)",
    )

    version_mutex.add_argument(
        "--local",
        "-l",
        action="store_true",
        help="Determine the latest version using the latest available git-tag",
    )

    parser.add_argument(
        "--pre-release",
        help="Add the specified text as a pre-release identifier (don't include leading -)",
    )

    parser.add_argument(
        "--build-meta",
        help="Add the specified text as a build-metadata identifier (don't include leading +)",
    )

    parser.add_argument(
        "message",
        help="Text to be parsed as a Conventional Commit message",
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
    elif not args.silent:
        logger.add(sys.stderr, level="INFO")

    logger.info(f"Message:\n{args.message}")

    # Parse the commit message and compute the bump
    try:
        parsed_message = parse(args.message, args.config)
    except ParseException as err:
        logger.error(
            "Parsing of commit message failed! This is likely due to the message NOT being a valid Conventional Commit."
        )
        logger.error(f"Error: {err}")
        raise
    bump = calculate_bump(parsed_message)

    # Determine how to get ahold of the latest version
    semver = None
    if args.semver:
        logger.debug(
            f"Latest Semantic Version was provided as an argument: {args.semver}"
        )
        semver = args.semver

    elif args.local:
        logger.debug(
            "Latest Semantic Version will be fetched from the current git branch"
        )
        repo = Repo(Path.cwd())
        tags = sorted(repo.tags, key=lambda t: t.tag.tagged_date)
        try:
            semver = str(tags[-1])
        except Exception as err:
            if not tags:
                logger.error("There seems to be no tags in the repo!")
            else:
                logger.error("Something went wrong when attempting to fetch tags!")
            logger.error(f"Error: {err}")
            raise
        logger.info(f"Latest tag on current branch is: {semver}")

    else:
        logger.debug("No SemVer provided, defaulting to 0.0.0")
        semver = "0.0.0"

    new_version = calculate_new_version(semver, bump, args.pre_release, args.build_meta)

    logger.info(f"New version: {new_version}")
    print(new_version)


if __name__ == "__main__":
    main()
