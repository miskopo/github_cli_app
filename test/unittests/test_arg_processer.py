from argparse import ArgumentParser
from unittest import mock

from pytest import raises

from github.authentication import load_api_key, register_api_key
from github.github_controller import GithubController


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
    parser.add_argument("--no_numbers", action="store_true")
    parser.add_argument("--description")
    api_key = load_api_key()
    github_ctl = GithubController(None, api_key)

    def inner():
        return func(github_ctl, parser)
    return inner


@setup_controller_and_parser
def test_valid_options(github_ctl, parser):
    with mock.patch.object(GithubController, 'execute_arg') as mockingbird:
        mockingbird.return_value = None

        github_ctl.args = parser.parse_args(["register"])
        assert github_ctl.process_args()
        assert mockingbird.called_with(func=register_api_key)

        github_ctl.args = parser.parse_args(["list-my-repositories"])
        assert github_ctl.process_args()
        assert mockingbird.called_with(func=github_ctl.list_my_repositories)

        github_ctl.args = parser.parse_args(["list-user-repositories", "username"])
        assert github_ctl.process_args()
        assert mockingbird.called_with(func=github_ctl.list_user_repositories)

        github_ctl.args = parser.parse_args(["create-repository"])
        assert github_ctl.process_args()
        assert mockingbird.called_with(func=github_ctl.create_new_repository)

        github_ctl.args = parser.parse_args(["delete-repository"])
        assert github_ctl.process_args()
        assert mockingbird.called_with(func=github_ctl.delete_repository)

        github_ctl.args = parser.parse_args(["create-project"])
        assert github_ctl.process_args()
        assert mockingbird.called_with(func=github_ctl.create_new_project)


@setup_controller_and_parser
def test_invalid(github_ctl, parser):
    with mock.patch.object(GithubController, 'execute_arg') as mockingbird:
        github_ctl.args = parser.parse_args(["invalid"])
        assert not github_ctl.process_args()
        assert not mockingbird.called


@setup_controller_and_parser
def test_empty_args(github_ctl, parser):
    with mock.patch.object(GithubController, 'execute_arg') as mockingbird:
        with raises(SystemExit):
            github_ctl.args = parser.parse_args([])
            assert not github_ctl.process_args()
            assert not mockingbird.called

