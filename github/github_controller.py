from .authentication import load_api_key
from .common.InvalidAPIKeyException import InvalidAPIKeyException
from .logger import logger
from requests import post
from .api_forms.repositories import list_repositories
from json import loads


class GithubController:
    __slots__ = 'api_key', 'args'
    api_endpoint = 'https://api.github.com/graphql'

    def __init__(self, args):
        self.api_key = None
        self.args = args

    def __call__(self, *args, **kwargs):
        self.obtain_api_key()
        self.process_args()

    def obtain_api_key(self):
        """

        :return:
        """
        try:
            self.api_key = load_api_key()
        except FileNotFoundError:
            logger.warning("'api_key' file missing in project root. Please, create the file and add your API key to it")
            return False
        except InvalidAPIKeyException:
            logger.warning("'api_key' file present, but it's either missing the key or the key is malformed")
            return False

    def process_args(self):
        """

        :return:
        """
        actions_dict = {'list-my-repositories': self.list_my_repositories}
        for arg in self.args.action:
            if arg in actions_dict.keys():
                actions_dict[arg]()

    # Repositories operations

    def list_my_repositories(self):
        """

        :return:
        """
        with post(self.api_endpoint, json=list_repositories,
                  headers={"Authorization": "bearer {}".format(self.api_key)}) as response:
            if response.ok:
                for i in range(loads(response.text)['data']['viewer']['repositories']['totalCount']):
                    print("{}:".format(i))
                    print(loads(response.text)['data']['viewer']['repositories']['edges'][i]['node']['name'])
                    print(loads(response.text)['data']['viewer']['repositories']['edges'][i]['node']['sshUrl'])
                    print(loads(response.text)['data']['viewer']['repositories']['edges'][i]['node']['url'])
                    print()
