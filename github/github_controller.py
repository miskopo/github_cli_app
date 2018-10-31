from json import loads

from requests import post

from .api_forms.repositories import list_repositories, list_user_repositories
from .authentication import load_api_key
from .cli_printer import CLIPrinter
from .common.InvalidAPIKeyException import InvalidAPIKeyException
from .common.InvalidNumberOfArgumentsException import InvalidNumberOfArgumentsException
from .common.deprecated_decorator import deprecated
from .logger import logger


class GithubController:
    __slots__ = 'api_key', 'args'
    graphql_api_endpoint = 'https://api.github.com/graphql'
    rest_api_base_url = 'https://api.github.com'

    def __init__(self, args):
        self.api_key = None
        self.args = args

    def __call__(self, *args, **kwargs):
        if not self.obtain_api_key():
            return False
        self.process_args()

    def obtain_api_key(self) -> bool:
        """
        Method invokes 'load_api_key' function and saves obtained API key into class attribute

        # TODO: Long desc
        :return: True, if the API key was successfully saved into class attribute, False otherwise

        or the API key is malformed
        """
        try:
            self.api_key = load_api_key()
            return True
        except FileNotFoundError:
            logger.warning("'api_key' file missing in project root. Please, create the file and add your API key to it")
            return False
        except InvalidAPIKeyException:
            logger.warning("Environmental variable 'GITHUB_API_KEY' or 'api_key' file present, "
                           "but it's either missing the key or the key is malformed")
            return False

    def process_args(self):
        """

        :return:
        """
        actions_dict = {
            'list-my-repositories': self.list_my_repositories,
            'list-user-repositories' : self.list_user_list_repositories
        }
        for arg in self.args.action:
            # TODO: Investigate
            if arg in actions_dict.keys():
                CLIPrinter.out(actions_dict[arg](), self.args)

    # Repositories operations
    def general_repositories_request(self, json_data):
        """
        Common method for repositories listing request
        :param json_data: json to be sent
        :return: API response
        """
        with post(self.graphql_api_endpoint, json=json_data,
                  headers={"Authorization": "bearer {}".format(self.api_key)}) as response:
            logger.debug("Response status code: {}".format(response.status_code))
            if response.ok and loads(response.text)['data']:
                return response
            else:
                logger.error("Error occurred, response status code {}, message {}".format(response.status_code,
                                                                                          loads(response.text)['errors']
                                                                                          ))

    def general_repositories_output_returner(self, repositories_dict) -> [(str, str, str)]:
        """
        Common return method for repositories listing methods.

        Method packs provided results of queries into list of tuples (name, sshUrl, url)
        :param repositories_dict: 'edges' part of the API response
        :return:
        """
        return [
            (
                edge['node']['name'] if not self.args.url_only else "",
                edge['node']['sshUrl'] if not self.args.https else "",
                edge['node']['url'] if self.args.https else "")
            for edge in repositories_dict
        ]

    @deprecated
    def list_my_repositories(self) -> [(str, str, str)]:
        """
        List all repositories of the current user (authenticated by API key)

        :return: list of repositories in tuples (name, sshUrl, url)
        """
        response = self.general_repositories_request(list_repositories)
        total_number_of_repositories = loads(response.text)['data']['viewer']['repositories']['totalCount']
        logger.debug("Total number of repositories obtainable: {}".format(total_number_of_repositories))
        repositories_dict = loads(response.text)['data']['viewer']['repositories']['edges']
        return self.general_repositories_output_returner(repositories_dict)

    @deprecated
    def list_user_list_repositories(self):
        """
        Lists repositories of selected user

        Method sends request for repositories of user provided in argument after 'list-user-repositories' keyword.
        In case this user does not exist, method returns error message from Github.
        :return: list of repositories in tuples (name, sshUrl, url) for selected user or Github's error message in case
        of failure
        """
        if len(self.args.action) != 2:
            raise InvalidNumberOfArgumentsException()
        # I am truly sorry for the replace, right now I can't think of anything else
        list_user_repositories['query'] = list_user_repositories['query'].replace("username_placeholder",
                                                                                  self.args.action[1])
        response = self.general_repositories_request(list_user_repositories)
        # isn't it weird that you get status 200 even in case of error?
        try:
            error_message = loads(response.text)['errors']
            logger.error(error_message)
            return "Github replies: {}".format(error_message)
        except KeyError:
            pass
        total_number_of_repositories = loads(response.text)['data']['user']['repositories']['totalCount']
        logger.debug("Total number of repositories obtainable: {}".format(total_number_of_repositories))
        repositories_dict = loads(response.text)['data']['user']['repositories']['edges']
        return self.general_repositories_output_returner(repositories_dict)


