#! /bin/bash -xe

# Convenience file to keep all integration related tools in one place.
# This script can be invoked both from your development environment:
# and is also invoked as a GitHub Action on every Pull Request.

poetry run black src/ tests/ --check
poetry run flake8 --ignore=E501 src/ tests/
poetry run pytest tests/
poetry run bats tests/integration.bats