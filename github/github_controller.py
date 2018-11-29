from json import loads

from requests import post, get, delete, Response

from .authentication import load_api_key
from .cli_printer import CLIPrinter
from .common import InvalidAPIKeyException, InvalidNumberOfArgumentsException, deprecated, \
    check_qraphql_response
from .logger import logger
from .queries.graphQL_mutation import ViewerMutation
from .queries.graphQL_query import ViewerQuery, UserQuery


class GithubController:
    __slots__ = 'api_key', 'args'
    graphql_api_endpoint = 'https://api.github.com/graphql'
    rest_api_endpoint = 'https://api.github.com'

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

    def process_args(self) -> bool:
        """
        Method executes function assigned to argument provided by user

        :return: True if the execution was successful, False otherwise
        """
        actions_dict = {
            'list-my-repositories': self.list_my_repositories,
            'list-user-repositories': self.list_user_list_repositories,
            'create-repository': self.create_new_repository,
            'delete-repository': self.delete_repository,
            'create-project': self.create_new_project
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

    def send_graphql_request(self, json_data) -> Response:
        """
        Common method for repositories listing request
        :param json_data: json to be sent
        :return: API response
        """
        with post(self.graphql_api_endpoint, json=json_data,
                  headers={"Authorization": f"bearer {self.api_key}"}) as response:
            logger.debug(f"Response status code: {response.status_code}")
            if check_qraphql_response(response)[0]:
                return response
            else:
                raise ValueError(f"{check_qraphql_response(response)[1]}")

    def send_restful_request(self, endpoint, json_data, method='GET') -> Response:
        header = {"Authorization": f"token {self.api_key}"}
        if method == 'GET':
            with get(endpoint, json=json_data, headers=header) as response:
                logger.debug(f"Response status code: {response.status_code}")
        elif method == 'POST':
            with post(endpoint, json=json_data, headers=header) as response:
                logger.debug(f"Response status code: {response.status_code}")
        elif method == 'DELETE':
            with delete(endpoint, headers=header) as response:
                logger.debug(f"Response status code: {response.status_code}")
        else:
            response = None
        return response

    def list_my_repositories(self):
        """
        Methods lists repositories of current user authenticated by API key

        :return: List of repositories or error response in case of error
        """
        list_repositories = ViewerQuery(('repositories', ['name', 'url', 'sshUrl']))
        list_repositories.construct_query()
        logger.debug(list_repositories.__dict__())
        try:
            response = self.send_graphql_request(list_repositories.__dict__())
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
            response = self.send_graphql_request(list_user_repositories.__dict__())
            return self.repositories_output_list_packer(loads(response.text)['data']['user']['repositories']['edges'])
        except ValueError as e:
            return str(e)

    @deprecated
    def create_new_project(self):
        if len(self.args.action) != 2:
            raise InvalidNumberOfArgumentsException()

        try:
            # FIXME: Needs to work with repo id, not user id
            logger.debug("Obtaining viewer's id")
            viewer_id = loads(self.send_graphql_request(ViewerMutation.obtain_viewer_id_query()).text)['data']['viewer']['id']
        except ValueError as e:
            return str(e)
        create_new_repository = ViewerMutation(
            ('createProject', {'ownerId': viewer_id, 'name': self.args.action[1]}))
        create_new_repository.construct_query()
        logger.debug(create_new_repository.__dict__())
        try:
            self.send_graphql_request(create_new_repository.__dict__())
            return f"Repository created successfully"
        except ValueError as e:
            return str(e)

    def create_new_repository(self):
        """
        Creates new repository
        :return: Message describing operation result
        """
        json = {"name": self.args.action[1],
                "description": self.args.description[0] if self.args.description else "",
                "private": self.args.private if self.args.private else False}
        response = self.send_restful_request(endpoint=f"{self.rest_api_endpoint}/user/repos",
                                             json_data=json, method="POST")
        if response.status_code == 422:
            logger.debug("Repository already exists")
            return f"Repository with name {self.args.action[1]} already exists"
        return [(loads(response.text)['name'], loads(response.text)['ssh_url'], loads(response.text)['git_url'])]

    def delete_repository(self):
        """
        Delete repository
        :return: Message describing operation result
        """
        response = self.send_restful_request(endpoint=f"{self.rest_api_endpoint}/repos/miskopo/{self.args.action[1]}",
                                             json_data=None, method='DELETE')
        if response.status_code == 204:
            return f"Repository {self.args.action[1]} was deleted successfully"
        else:
            return f"Unable to delete repository {self.args.action[1]}: {loads(response.text)['message']}"

