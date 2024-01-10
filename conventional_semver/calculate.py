"""This module contains the functions required to calculate the next Semantic Version."""
from loguru import logger
from semantic_version import Version


def calculate_bump(parsed_message):
    """Calculate which of the SemVer parts should be bumped.

    The parsed_message is a ConventionalCommitRunner() from PCCC.

    The following mapping between [type] and [bump] is used:

    Type         | Bump
    -------------+-----
    <any valid>  | patch
    feat         | minor
    <any valid>! | major

    And as described in the specification, the BREAKING CHANGE and BREAKING-CHANGE
    footer will also result in a major bump.

    Specification: https://www.conventionalcommits.org/en/v1.0.0/#specification
    """

    # If the commit message indicates that the change is breaking we can return
    if parsed_message.breaking["flag"] or parsed_message.breaking["token"]:
        return "MAJOR"

    # If the commit message is of type 'feat' we can return
    if parsed_message.header["type"] == "feat":
        return "MINOR"

    # If neither breaking nor a new feature, it's a patch.
    return "PATCH"


def calculate_new_version(version, bump, pre="", build=""):
    """Given a SemVer and a bump, increment the version according to the SemVer spec.

    Specification: https://semver.org/#semantic-versioning-specification-semver
    """
    semver = Version(version)

    new_base = None
    if bump == "MAJOR":
        new_base = semver.next_major()
        logger.info("Incrementing the MAJOR version.")

    if bump == "MINOR":
        new_base = semver.next_minor()
        logger.info("Incrementing the MINOR version.")

    if bump == "PATCH":
        new_base = semver.next_patch()
        logger.info("Incrementing the PATCH version.")

    if new_base is None:
        logger.error(
            f"Unable to calculate new version for version {version} and bump {bump}!"
        )
        raise

    # Stitch together a new version depending on whether pre-release, build metadata
    # or neither was provided.
    # The semantic-version lib dictates that prerelease and build are passed as tuples, hence the split.
    if pre and build:
        return Version(
            major=new_base.major,
            minor=new_base.minor,
            patch=new_base.patch,
            prerelease=pre.split("."),
            build=build.split("."),
        )
    if pre:
        return Version(
            major=new_base.major,
            minor=new_base.minor,
            patch=new_base.patch,
            prerelease=pre.split("."),
        )
    if build:
        return Version(
            major=new_base.major,
            minor=new_base.minor,
            patch=new_base.patch,
            build=build.split("."),
        )

    return Version(major=new_base.major, minor=new_base.minor, patch=new_base.patch)
