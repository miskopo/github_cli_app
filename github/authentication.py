from .logger import logger
from .common.InvalidAPIKeyException import InvalidAPIKeyException


def load_api_key():
    try:
        with open('../api_key') as key_file:
            api_key = key_file.readline().strip()
            if not api_key or len(api_key) != 40:
                raise InvalidAPIKeyException
            logger.debug("Obtained API key from file")
            return api_key
    except FileNotFoundError:
        logger.error("API key file not found")
        raise


def register_api_key():
    pass
