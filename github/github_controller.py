from json import loads

from requests import post

from .api_forms.repositories import list_repositories
from .authentication import load_api_key
from .cli_printer import CLIPrinter
from .common.InvalidAPIKeyException import InvalidAPIKeyException
from .logger import logger


class GithubController:
    __slots__ = 'api_key', 'args'
    api_endpoint = 'https://api.github.com/graphql'

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
        actions_dict = {'list-my-repositories': self.list_my_repositories}
        for arg in self.args.action:
            # TODO: Investigate
            if arg in actions_dict.keys():
                CLIPrinter.out(actions_dict[arg](), self.args)

    # Repositories operations

    def list_my_repositories(self) -> [(str, str, str)]:
        """
        List all repositories of the current user (authenticated by API key)

        :return: list of tuples (name, sshUrl, url)
        """
        with post(self.api_endpoint, json=list_repositories,
                  headers={"Authorization": "bearer {}".format(self.api_key)}) as response:
            logger.debug("Response status code: {}".format(response.status_code))
            if response.ok and loads(response.text)['data']:
                total_number_of_repositories = loads(response.text)['data']['viewer']['repositories']['totalCount']
                logger.debug("Total number of repositories obtainable: {}".format(total_number_of_repositories))
                repositories_dict = loads(response.text)['data']['viewer']['repositories']['edges']
                return [
                    (
                        repositories_dict[i]['node']['name'] if not self.args.url_only else "",
                        repositories_dict[i]['node']['sshUrl'] if not self.args.https else "",
                        repositories_dict[i]['node']['url'] if self.args.https else "")
                    for i in range(total_number_of_repositories)
                ]
            else:
                logger.error("Error occurred, response status code {}, message {}".format(response.status_code,
                                                                                          loads(response.text)['errors']
                                                                                          ))

