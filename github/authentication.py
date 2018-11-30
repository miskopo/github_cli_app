from os import environ
from os.path import dirname

import github
from github.common import InvalidAPIKeyException
from github.logger import logger


def load_api_key():
    """
    Function loads Github API key either from environmental variable 'GITHUB_API_KEY' or from file 'api_key' in
    project's root.

    Functions checks for system environmental variable called 'GITHUB_API_KEY' and if it exists, it checks whether this
    variable is correct. If so, it's returned. If no 'GITHUB_AIP_KEY' variable is found, function looks for file
    'api_key' in the project's root directory. In case it's found, its content is loaded anc checked. If everything is
    all-right, value is returned. If not, exception is raised.
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
        logger.debug("No environ variable GITHUB_API_KEY")
    else:
        return api_key
    try:
        with open(f'{dirname(github.__file__)}/../api_key') as key_file:
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
