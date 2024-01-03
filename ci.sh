#! /bin/bash -xe

# Convenience file to keep all integration related tools in one place.
# This script can be invoked both from your development environment:
# and is also invoked as a GitHub Action on every Pull Request.

poetry run black conventional_semver/ --check
poetry run flake8 conventional_semver/ tests/
poetry run pytest tests/