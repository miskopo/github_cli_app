from json import loads

from requests import post

from .queries.graphQL_query import ViewerQuery, UserQuery
from .queries.graphQL_mutation import ViewerMutation
from .authentication import load_api_key
from .cli_printer import CLIPrinter
from .common import InvalidAPIKeyException, InvalidNumberOfArgumentsException
from .logger import logger


class GithubController:
    __slots__ = 'api_key', 'args'
    graphql_api_endpoint = 'https://api.github.com/graphql'

    def __init__(self, args):
        self.api_key = None
        self.args = args

    def __call__(self, *args, **kwargs):
        if not self.obtain_api_key():
            return False
        return self.process_args()

    def obtain_api_key(self) -> bool:
        """
        Method invokes 'load_api_key' function and saves obtained API key into class attribute

        :return: True, if the API key was successfully saved into class attribute, False otherwise
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

    @staticmethod
    def check_response(response) -> (bool, str):
        """
        Method checks for error message in response, as github return 200 even in case of error
        :param response: response to be checked
        :return: True if there is no error in response, False otherwise
        """
        if response and response.ok:
            try:
                error_message = loads(response.text)['errors']
            except (TypeError, KeyError):
                return True, None
            else:
                return False, error_message
        else:
            return False, "No response"

    def process_args(self) -> bool:
        """
        Method executes function assigned to argument provided by user

        :return: True if the execution was successful, False otherwise
        """
        actions_dict = {
            'list-my-repositories': self.list_my_repositories,
            'list-user-repositories': self.list_user_list_repositories,
            'create-repository': self.create_new_repository
        }
        if self.args.action[0] in actions_dict.keys():
            CLIPrinter.out(actions_dict[self.args.action[0]](), self.args)
            return True
        return False

    def repositories_output_list_packer(self, repositories_dict) -> [(str, str, str)]:
        """
        Method packs output from repository listing into list of tuples (name, sshUrl, url) respecting provided flags
        :param repositories_dict: dictionary of edges from response
        :return: list of tuples (name, sshUrl, url) for each repository
        """
        return [
            (
                edge['node']['name'] if not self.args.url_only else "",
                edge['node']['sshUrl'] if not self.args.https else "",
                edge['node']['url'] if self.args.https else "")
            for edge in repositories_dict
        ]

    def send_request(self, json_data):
        """
        Common method for repositories listing request
        :param json_data: json to be sent
        :return: API response
        """
        with post(self.graphql_api_endpoint, json=json_data,
                  headers={"Authorization": "bearer {}".format(self.api_key)}) as response:
            logger.debug("Response status code: {}".format(response.status_code))
            if self.check_response(response)[0]:
                return response
            else:
                raise ValueError(f"{self.check_response(response)[1]}")

    def list_my_repositories(self):
        """
        Methods lists repositories of current user authenticated by API key

        :return: List of repositories or error response in case of error
        """
        list_repositories = ViewerQuery(('repositories', ['name', 'url', 'sshUrl']))
        list_repositories.construct_query()
        logger.debug(list_repositories.__dict__())
        try:
            response = self.send_request(list_repositories.__dict__())
            return self.repositories_output_list_packer(loads(response.text)['data']['viewer']['repositories']['edges'])
        except ValueError as e:
            return str(e)

    def list_user_list_repositories(self):
        """
        Method lists repositories of user provided in argument
        :return: List of user's repositories or error response in case of error (e.g. wrong username)
        """

        if len(self.args.action) != 2:
            raise InvalidNumberOfArgumentsException()

        list_user_repositories = UserQuery(('repositories', ['name', 'url', 'sshUrl']), username=self.args.action[1])
        list_user_repositories.construct_query()
        try:
            response = self.send_request(list_user_repositories.__dict__())
            return self.repositories_output_list_packer(loads(response.text)['data']['user']['repositories']['edges'])
        except ValueError as e:
            return str(e)

    def create_new_repository(self):
        # MDQ6VXNlcjQzODc1OTA0
        if len(self.args.action) != 2:
            raise InvalidNumberOfArgumentsException()

        create_new_repository = ViewerMutation(
            ('createProject', {'ownerId': "MDQ6VXNlcjQzODc1OTA0", 'name': self.args.action[1]}))
        create_new_repository.construct_query()
        logger.debug(create_new_repository.__dict__())
        try:
            response = self.send_request(create_new_repository.__dict__())
            return "Succ"
        except ValueError as e:
            return str(e)
