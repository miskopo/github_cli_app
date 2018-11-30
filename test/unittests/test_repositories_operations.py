from argparse import ArgumentParser
from logging import disable as disable_logger, CRITICAL
from unittest import mock

from pytest import raises

from github.authentication import load_api_key
from github.common import InvalidNumberOfArgumentsException
from github.github_controller import GithubController

disable_logger(CRITICAL)


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def setup_controller_and_parser(func):
    parser = ArgumentParser()
    parser.add_argument("action", nargs=1)
    parser.add_argument("parameters", nargs="*")
    parser.add_argument("--both_urls", action="store_true")
    parser.add_argument("--url_only", action="store_true")
    parser.add_argument("--https", action="store_true")
    parser.add_argument("--private", action="store_true")
    parser.add_argument("--description")
    api_key = load_api_key()
    github_ctl = GithubController(None, api_key)

    def inner():
        return func(github_ctl, parser)
    return inner


@setup_controller_and_parser
def test_list_my_repositories(github_ctl, arg_parser):
    with mock.patch.object(GithubController, 'send_graphql_request') as mockingbird:
        mockingbird.return_value = Namespace(text='{"data":{"viewer":{"repositories":{"totalCount":2,"edges":[{'
                                                  '"node":{"name":"test_repo1","url":"https://repo1",'
                                                  '"sshUrl":"ssh:repo1"}},{"node":{"name":"test_repo2",'
                                                  '"url":"https://repo2","sshUrl":"ssh:repo2"}}]}}}}')
        github_ctl.args = arg_parser.parse_args(["dummy", "--both_urls"])
        assert github_ctl.list_my_repositories() == [("test_repo1", "ssh:repo1", "https://repo1"),
                                                     ("test_repo2", "ssh:repo2", "https://repo2")]
        github_ctl.args = arg_parser.parse_args(["dummy", "--https"])
        assert github_ctl.list_my_repositories() == [("test_repo1", "", "https://repo1"),
                                                     ("test_repo2", "", "https://repo2")]
        github_ctl.args = arg_parser.parse_args(["dummy", "--url_only"])
        assert github_ctl.list_my_repositories() == [("", "ssh:repo1", ""),
                                                     ("", "ssh:repo2", "")]
        github_ctl.args = arg_parser.parse_args(["dummy", "--url_only", "--both_urls"])
        assert github_ctl.list_my_repositories() == [("", "ssh:repo1", "https://repo1"),
                                                     ("", "ssh:repo2", "https://repo2")]


@setup_controller_and_parser
def test_user_repositories(github_ctl, arg_parser):
    with mock.patch.object(GithubController, 'send_graphql_request') as mockingbird:
        mockingbird.return_value = Namespace(text='{"data":{"user":{"repositories":{"totalCount":2,"edges":[{'
                                                  '"node":{"name":"test_user_repo1","url":"https://user_repo1",'
                                                  '"sshUrl":"ssh:user_repo1"}},{"node":{"name":"test_user_repo2",'
                                                  '"url":"https://user_repo2","sshUrl":"ssh:user_repo2"}}]}}}}')
        github_ctl.args = arg_parser.parse_args([""])
        with raises(InvalidNumberOfArgumentsException):
            github_ctl.list_user_repositories()

        github_ctl.args = arg_parser.parse_args(["action"])
        with raises(InvalidNumberOfArgumentsException):
            github_ctl.list_user_repositories()

        github_ctl.args = arg_parser.parse_args(["action", "user", "--both_urls"])
        assert github_ctl.list_user_repositories() == [("test_user_repo1", "ssh:user_repo1", "https://user_repo1"),
                                                       ("test_user_repo2", "ssh:user_repo2", "https://user_repo2")]
        github_ctl.args = arg_parser.parse_args(["action", "user", "--https"])
        assert github_ctl.list_user_repositories() == [("test_user_repo1", "", "https://user_repo1"),
                                                       ("test_user_repo2", "", "https://user_repo2")]
        github_ctl.args = arg_parser.parse_args(["action", "user", "--url_only"])
        assert github_ctl.list_user_repositories() == [("", "ssh:user_repo1", ""),
                                                       ("", "ssh:user_repo2", "")]
        github_ctl.args = arg_parser.parse_args(["action", "user", "--url_only", "--both_urls"])
        assert github_ctl.list_user_repositories() == [("", "ssh:user_repo1", "https://user_repo1"),
                                                       ("", "ssh:user_repo2", "https://user_repo2")]


@setup_controller_and_parser
def test_create_repo(github_ctl, arg_parser):
    with mock.patch.object(GithubController, 'send_restful_request') as restful_mockingbird:
        # https://tinyurl.com/resting-mockingbird
        restful_mockingbird.return_value = Namespace(text='{"name": "new_repo",'
                                                          '"ssh_url": "ssh:new_repo",'
                                                          '"git_url": "git:http_repo"}',
                                                     status_code=200)
        github_ctl.args = arg_parser.parse_args([""])
        with raises(InvalidNumberOfArgumentsException):
            github_ctl.create_new_repository()

        github_ctl.args = arg_parser.parse_args(["action"])
        with raises(InvalidNumberOfArgumentsException):
            github_ctl.list_user_repositories()

        github_ctl.args = arg_parser.parse_args(["action", "new_repo"])
        assert github_ctl.create_new_repository() == [("new_repo", "ssh:new_repo", "git:http_repo")]

        json = {"name": "new_repo",
                "description": "",
                "private": False}
        restful_mockingbird.assert_called_with(endpoint="https://api.github.com/user/repos",
                                               json_data=json, method='POST')

        restful_mockingbird.return_value = Namespace(text='{"name": "new_repo",'
                                                          '"ssh_url": "ssh:new_repo",'
                                                          '"git_url": "git:http_repo"}',
                                                     status_code=422)
        assert github_ctl.create_new_repository() != [("new_repo", "ssh:new_repo", "git:http_repo")]
        assert all(x in github_ctl.create_new_repository().lower() for x in ["new_repo", "exists"])


@setup_controller_and_parser
def test_delete_repository(github_ctl, arg_parser):
    with mock.patch.object(GithubController, 'send_restful_request') as restful_mockingbird:
        with mock.patch.object(GithubController, 'send_graphql_request') as username_mock:
            username_mock.return_value = Namespace(text='{"data": {"viewer": {"login": "mock_user"}}}')
            restful_mockingbird.return_value = Namespace(status_code=204)
            github_ctl.args = arg_parser.parse_args([""])
            with raises(InvalidNumberOfArgumentsException):
                github_ctl.delete_repository()

            github_ctl.args = arg_parser.parse_args(["action"])
            with raises(InvalidNumberOfArgumentsException):
                github_ctl.delete_repository()

            github_ctl.args = arg_parser.parse_args(["action", "deleted_repo"])
            assert all(x in github_ctl.delete_repository().lower() for x in ["deleted_repo", "deleted"])

            restful_mockingbird.return_value = Namespace(status_code=404, text='{"message": "Not found"}')
            assert all(x in github_ctl.delete_repository().lower() for x in ["deleted_repo", "unable"])

            restful_mockingbird.assert_called_with(endpoint="https://api.github.com/repos/mock_user/deleted_repo",
                                                   json_data=None, method='DELETE')
