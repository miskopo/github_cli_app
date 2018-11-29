from argparse import ArgumentParser
from logging import disable as disable_logger, CRITICAL
from unittest import mock

from authentication import load_api_key
from github.github_controller import GithubController

disable_logger(CRITICAL)


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def setup_controller(func):
    parser = ArgumentParser()
    parser.add_argument("--both_urls", action="store_true")
    parser.add_argument("--url_only", action="store_true")
    parser.add_argument("--https", action="store_true")
    args = parser.parse_args(["--both_urls"])
    api_key = load_api_key()
    github_ctl = GithubController(args, api_key)

    def inner():
        return func(github_ctl)
    return inner


@setup_controller
def test_list_my_repositories(github_ctl):
    with mock.patch.object(GithubController, 'send_graphql_request') as mockingbird:
        mockingbird.return_value = Namespace(text='{"data":{"viewer":{"repositories":{"totalCount":2,"edges":[{'
                                                  '"node":{"name":"test_repo1","url":"https://repo1",'
                                                  '"sshUrl":"ssh:repo1"}},{"node":{"name":"test_repo2",'
                                                  '"url":"https://repo2","sshUrl":"ssh:repo2"}}]}}}}')
        assert github_ctl.list_my_repositories() == [("test_repo1", "ssh:repo1", "https://repo1"),
                                                     ("test_repo2", "ssh:repo2", "https://repo2")]
