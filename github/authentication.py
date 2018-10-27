from os import environ
from os.path import dirname

import github
from .common.InvalidAPIKeyException import InvalidAPIKeyException
from .logger import logger


def load_api_key():
    """
    Function loads Github API key either from environmental variable 'GITHUB_API_KEY' or from file 'api_key' in
    project's root.

    # TODO: Long desc
    :return: API key, if it was successfully obtained
    :raise: FileNotFoundError in case the 'api_key' file is missing completely
    :raise: InvalidAPIKeyException in case the 'api_key' file exist, but is either missing the API key
    """
    # First try, whether environmental variable 'GITHUB_API_KEY' exists
    try:
        api_key = environ['GITHUB_API_KEY']
        if len(api_key) != 40:
            raise InvalidAPIKeyException
    except KeyError:
        # If it doesn't exist, however, it's not big deal
        pass
    else:
        return api_key
    try:
        with open('{}/../api_key'.format(dirname(github.__file__))) as key_file:
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
