from pathlib import Path

from loguru import logger
import pccc
from pccc.config import _load_file


def _get_config(config_file):
    """Set the configuration for the PCCC CCR.

    In order to circumvent the _create_argument_parser() call used by Config()
    we hack around a little bit.

    From the PCCC code we see that _load_file will load a configuration file,
    defaulting to the first loadable file of ``pyproject.toml``, ``pccc.toml``,
    ``package.json``, ``pccc.json``, ``pccc.yaml``, ``pccc.yml``, and finally
    ``pccc.besp``.
    """
    config = pccc.Config()
    config.update(**_load_file(config_file))
    return config


def parse(message, config_file):
    """Use The Python Conventional Commit Parser to parse the commit message.

    If the ccr.parse() call is NOT successful an Exception will be raised.
    """

    ccr = pccc.ConventionalCommitRunner()

    config_file_path = Path(config_file)
    if not config_file_path.is_file():
        logger.error(f"Config file: {config_file_path} does not seem to exist!")
        logger.warning(
            "The script will attempt to look for config files in the PCCC default places."
        )
        config_file = None

    try:
        ccr.options = _get_config(config_file)
    except Exception:
        logger.error("The script was unable to find a config file to use!")
        raise

    ccr.raw = message.strip()
    ccr.clean()
    ccr.parse()
    logger.info("Message was successfully parsed!")

    logger.debug(f'Type: {ccr.header["type"]}')
    logger.debug(f'Has breaking !: {ccr.breaking["flag"]}')
    logger.debug(f'Has breaking token: {ccr.breaking["token"]}')
    logger.debug(f'Scope: {ccr.header["scope"]}')
    logger.debug(f'Description: {ccr.header["description"]}')
    logger.debug(f'Body: {ccr.body["paragraphs"]}')
    logger.debug(f"Footers: {ccr.footers}")

    return ccr
