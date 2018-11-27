from json import loads

from requests import post

from queries.graphQL_query import ViewerQuery, UserQuery
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
        self.process_args()

    def obtain_api_key(self) -> bool:
        """
        Method invokes 'load_api_key' function and saves obtained API key into class attribute

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

    @staticmethod
    def check_response(response) -> bool:
        """
        Method checks for error message in response, as github return 200 even in case of error
        :param response: response to be checked
        :return: True if there is no error in response, False otherwise
        """
        if response:
            if response.ok:
                try:
                    loads(response.text)['data']
                except (TypeError, KeyError):
                    pass
                else:
                    return True
            try:
                error_message = loads(response.text)['errors']
                logger.error(error_message)
            except (TypeError, KeyError):
                return True
            else:
                return False

    def process_args(self):
        """

        :return:
        """
        actions_dict = {
            'list-my-repositories': self.list_my_repositories,
            'list-user-repositories': self.list_user_list_repositories
        }
        for arg in self.args.action:
            if arg in actions_dict.keys():
                CLIPrinter.out(actions_dict[arg](), self.args)

    def output_list_packer(self, repositories_dict) -> [(str, str, str)]:
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
            if self.check_response(response):
                return response
            else:
                return None

    def list_my_repositories(self):
        list_repositories = ViewerQuery({'repositories': ['name', 'url', 'sshUrl']})
        list_repositories.construct_query()
        response = self.send_request(list_repositories.__dict__())
        if self.check_response(response):
            return self.output_list_packer(loads(response.text)['data']['viewer']['repositories']['edges'])
        else:
            return f"GitHub replies: {loads(response.text)['errors']}"

    def list_user_list_repositories(self):

        if len(self.args.action) != 2:
            raise InvalidNumberOfArgumentsException()

        list_user_repositories = UserQuery({'repositories': ['name', 'url', 'sshUrl']}, username=self.args.action[1])
        list_user_repositories.construct_query()

        response = self.send_request(list_user_repositories.__dict__())
        if self.check_response(response):
            return self.output_list_packer(loads(response.text)['data']['user']['repositories']['edges'])
        else:
            return f"GitHub replies: {loads(response.text)['errors']}"


