from json import loads

from requests import post, get, delete, Response

from .authentication import load_api_key, register_api_key
from .cli_printer import CLIPrinter
from .common import InvalidAPIKeyException, InvalidNumberOfArgumentsException, check_qraphql_response
from .logger import logger
from .queries.graphQL_mutation import ViewerMutation
from .queries.graphQL_query import ViewerQuery, UserQuery


class GithubController:
    __slots__ = 'api_key', 'args'
    graphql_api_endpoint = 'https://api.github.com/graphql'
    rest_api_endpoint = 'https://api.github.com'

    def __init__(self, args, api_key=None):
        self.api_key = api_key
        self.args = args

    def __call__(self, *args, **kwargs):
        if not self.api_key and not self.obtain_api_key():
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
        Method invokes execution of function assigned to argument provided by user

        :return: True if the execution was successful, False otherwise
        """
        actions_dict = {
            'register': register_api_key,
            'list-my-repositories': self.list_my_repositories,
            'list-user-repositories': self.list_user_repositories,
            'create-repository': self.create_new_repository,
            'delete-repository': self.delete_repository,
            'create-project': self.create_new_project
        }

        if self.args and self.args.action and self.args.action[0] in actions_dict.keys():
            self.execute_arg(actions_dict[self.args.action[0]])
            return True
        return False

    def execute_arg(self, func):
        """
        Executes function provided as argument
        :param func: function to be executed
        :return: None, CLIPrinter is invoked with provided function
        """
        CLIPrinter.out(func(), self.args)

    def repositories_output_list_packer(self, repositories_dict) -> [(str, str, str)]:
        """
        Method packs output from repository listing into list of tuples (name, sshUrl, url) respecting provided flags
        :param repositories_dict: dictionary of edges from response
        :return: list of tuples (name, sshUrl, url) for each repository
        """
        return [
            (
                edge['node']['name'] if not self.args.url_only else "",
                edge['node']['sshUrl'] if (not self.args.https or self.args.both_urls) else "",
                edge['node']['url'] if self.args.https or self.args.both_urls else "")
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
        """
        Method sends REST request of provided type to provided endpoint with provided data
        :param endpoint: REST endpoint
        :param json_data: json to be sent
        :param method: GET, POST, PUT or DELETE
        :return: API response
        """
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
            logger.debug(response.text)
            return self.repositories_output_list_packer(loads(response.text)['data']['viewer']['repositories']['edges'])
        except ValueError as e:
            return str(e)

    def list_user_repositories(self):
        """
        Method lists repositories of user provided in argument
        :return: List of user's repositories or error response in case of error (e.g. wrong username)
        """

        if not self.args.parameters:
            raise InvalidNumberOfArgumentsException()

        list_user_repositories = UserQuery(('repositories', ['name', 'url', 'sshUrl']),
                                           username=self.args.parameters[0])
        list_user_repositories.construct_query()
        try:
            response = self.send_graphql_request(list_user_repositories.__dict__())
            return self.repositories_output_list_packer(loads(response.text)['data']['user']['repositories']['edges'])
        except ValueError as e:
            return str(e)

    def create_new_project(self):
        """
        Creates new project under provided repository. Note: There can be multiple project with one name under one
        repository
        :return: Message describing operation result
        """
        if len(self.args.parameters) != 2:
            raise InvalidNumberOfArgumentsException()

        repo_id = loads(self.send_graphql_request(ViewerMutation.obtain_repository_id(self.args.parameters[0])).text)[
            'data']['viewer']['repository']['id']
        logger.debug(f"ID of repository {self.args.parameters[0]} is {repo_id}")
        create_new_repository = ViewerMutation(
            ('createProject', {'ownerId': repo_id, 'name': self.args.parameters[1]}))
        create_new_repository.construct_query()
        logger.debug(create_new_repository.__dict__())
        try:
            self.send_graphql_request(create_new_repository.__dict__())
            return f"Project {self.args.parameters[1]} created successfully in repository {self.args.parameters[0]}"
        except ValueError as e:
            return str(e)

    def create_new_repository(self):
        """
        Creates new repository
        :return: Message describing operation result
        """
        if not self.args.parameters:
            raise InvalidNumberOfArgumentsException()

        json = {"name": self.args.parameters[0],
                "description": self.args.description[0] if self.args.description else "",
                "private": self.args.private if self.args.private else False}
        response = self.send_restful_request(endpoint=f"{self.rest_api_endpoint}/user/repos",
                                             json_data=json, method="POST")
        if response.status_code == 422:
            logger.debug("Repository already exists")
            return f"Repository with name {self.args.parameters[0]} already exists"
        return [(loads(response.text)['name'], loads(response.text)['ssh_url'], loads(response.text)['git_url'])]

    def delete_repository(self) -> str:
        """
        Deletes repository
        :return: Message describing operation result
        """
        if not self.args.parameters:
            raise InvalidNumberOfArgumentsException()

        viewer_login = loads(self.send_graphql_request(ViewerMutation.obtain_viewer_login_query()).text)['data'][
            'viewer']['login']
        response = self.send_restful_request(endpoint=
                                             f"{self.rest_api_endpoint}/repos/{viewer_login}/{self.args.parameters[0]}",
                                             json_data=None, method='DELETE')
        if response.status_code == 204:
            return f"Repository {self.args.parameters[0]} was deleted successfully"
        else:
            return f"Unable to delete repository {self.args.parameters[0]}: {loads(response.text)['message']}"

