from getpass import getpass
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
    """
    Registers API KEY and stores it in API KEY file located in application's root

    If the key already exists, user is given choice whether to continue using already registered key or to register new
    key
    :return: Informative string
    """

    def register_the_key():
        _api_key = getpass("Please copy-paste (or type) you API KEY and press return. Characters will not be shown: ")
        if len(_api_key) != 40:
            raise InvalidAPIKeyException("Invalid length of API KEY (should be 40 characters)")
        try:
            with open(f'{dirname(github.__file__)}/../api_key', "w") as key_file:
                key_file.write(_api_key)
                logger.info("API KEY written to api_key file")
                return "API KEY successfully written to api_key file"
        except PermissionError as e:
            logger.error(str(e))
            return f"Error occurred: {str(e)}, key not written"

    try:
        load_api_key()
        logger.debug("API_KEY found")
        print("API Key already exists. Would you like to:")
        print("1. Keep using already registered key (default)")
        print("2. Register new key")
        attempts = 0
        while attempts < 4:
            choice = input("Your choice? ([1], 2): ") or "1"
            if choice == "1":
                return "Using already registered API KEY"
            elif choice == "2":
                register_the_key()
                return
            print("Invalid choice, please try again")
            attempts += 1
        return "Maximum attempts provided, exiting"
    except (FileNotFoundError, InvalidAPIKeyException):
        register_the_key()
