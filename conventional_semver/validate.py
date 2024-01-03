from loguru import logger
import pccc
from pccc.config import _load_file


def _get_config():
    """Set the configuration for the PCCC CCR.

    In order to circumvent the _create_argument_parser() call used by Config()
    we hack around a little bit.

    From the PCCC code we see that _load_file will load a configuration file,
    defaulting to the first loadable file of ``pyproject.toml``, ``pccc.toml``,
    ``package.json``, ``pccc.json``, ``pccc.yaml``, ``pccc.yml``, and finally
    ``pccc.besp``.
    """
    config = pccc.Config()
    config.update(**_load_file())

    #    logger.debug(f"Using configuration:\n{config}")

    return config


def parse(message):
    """Use The Python Conventional Commit Parser to parse the commit message.

    If the ccr.parse() call is NOT successful an Exception will be raised.
    """

    logger.debug(f"{message}")

    ccr = pccc.ConventionalCommitRunner()
    ccr.options = _get_config()

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
