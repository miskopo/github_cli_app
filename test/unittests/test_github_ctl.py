from argparse import ArgumentParser
from unittest import mock

from pytest import raises

from github.common import InvalidAPIKeyException
from github.github_controller import GithubController, CLIHandler


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
    github_ctl = GithubController(None, None)

    def inner():
        return func(github_ctl, parser)
    return inner


def mocked_request(*args, **kwargs):
    del args

    class MockResponse:
        def __init__(self, json_data=None, status_code=200):
            self.json_data = json_data
            self.status_code = status_code
            self.ok = status_code == 200
            self.text = '{"data": "lot_of_data"}' if self.ok else '{"errors": "lot_of_errors"}'

        def json(self):
            return self.json_data

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
    try:
        return MockResponse({'data': 'lot_of_data'}, 200) if kwargs['json'] else MockResponse(
            {'data': 'lot_of_data'}, 404)
    except KeyError:
        return MockResponse({'data': 'lot_of_data'}, 200)  # Delete statement does not have json


@setup_controller_and_parser
def test_obtain_api_key(github_ctl, parser):
    del parser
    with mock.patch('github.github_controller.load_api_key') as mockingbird:
        mockingbird.return_value = "1234567890123456789012345678901234567890"
        assert github_ctl.obtain_api_key()
        mockingbird.assert_called_once()
        assert github_ctl.api_key == mockingbird.return_value

    with mock.patch('github.github_controller.load_api_key') as mockingbird:
        mockingbird.side_effect = FileNotFoundError()
        assert not github_ctl.obtain_api_key()
        mockingbird.assert_called_once()

    with mock.patch('github.github_controller.load_api_key') as mockingbird:
        mockingbird.side_effect = InvalidAPIKeyException()
        assert not github_ctl.obtain_api_key()
        mockingbird.assert_called_once()


@setup_controller_and_parser
def test_graphql_request(github_ctl, parser):
    del parser
    with mock.patch('github.github_controller.post', side_effect=mocked_request) as post_request_mock:
        with raises(ValueError):
            github_ctl.send_graphql_request(json_data={})
        post_request_mock.assert_called_once()
        post_request_mock.assert_called_with('https://api.github.com/graphql',
                                             headers={'Authorization': 'bearer None'}, json={})

    with mock.patch('github.github_controller.post', side_effect=mocked_request) as post_request_mock:

        assert github_ctl.send_graphql_request(json_data={"data": "data"}).text == '{"data": "lot_of_data"}'
        post_request_mock.assert_called_once()
        post_request_mock.assert_called_with('https://api.github.com/graphql',
                                             headers={'Authorization': 'bearer None'}, json={"data": "data"})


@setup_controller_and_parser
def test_restful_request(github_ctl, parser):
    del parser
    with mock.patch('github.github_controller.post', side_effect=mocked_request) as post_request_mock:
        with mock.patch('github.github_controller.get', side_effect=mocked_request) as get_request_mock:
            with mock.patch('github.github_controller.delete', side_effect=mocked_request) as delete_request_mock:
                response = github_ctl.send_restful_request(endpoint="/end", json_data={"data": "data"}, method="GET")
                assert not post_request_mock.called
                assert get_request_mock.called
                assert not delete_request_mock.called
                get_request_mock.assert_called_with('/end', headers={'Authorization': 'token None'},
                                                    json={'data': 'data'})
                assert response

    with mock.patch('github.github_controller.post', side_effect=mocked_request) as post_request_mock:
        with mock.patch('github.github_controller.get', side_effect=mocked_request) as get_request_mock:
            with mock.patch('github.github_controller.delete', side_effect=mocked_request) as delete_request_mock:
                response = github_ctl.send_restful_request(endpoint="/end", json_data={"data": "data"}, method="POST")
                assert post_request_mock.called
                assert not get_request_mock.called
                assert not delete_request_mock.called
                post_request_mock.assert_called_with('/end', headers={'Authorization': 'token None'},
                                                     json={'data': 'data'})
                assert response

    with mock.patch('github.github_controller.post', side_effect=mocked_request) as post_request_mock:
        with mock.patch('github.github_controller.get', side_effect=mocked_request) as get_request_mock:
            with mock.patch('github.github_controller.delete', side_effect=mocked_request) as delete_request_mock:
                response = github_ctl.send_restful_request(endpoint="/end", json_data=None, method="DELETE")
                assert not post_request_mock.called
                assert not get_request_mock.called
                assert delete_request_mock.called
                delete_request_mock.assert_called_with('/end', headers={'Authorization': 'token None'})
                assert response

    with mock.patch('github.github_controller.post', side_effect=mocked_request) as post_request_mock:
        with mock.patch('github.github_controller.get', side_effect=mocked_request) as get_request_mock:
            with mock.patch('github.github_controller.delete', side_effect=mocked_request) as delete_request_mock:
                response = github_ctl.send_restful_request(endpoint="/end", json_data={"data": "data"},
                                                           method="NONSENSE")
                assert not post_request_mock.called
                assert not get_request_mock.called
                assert not delete_request_mock.called
                assert not response


@setup_controller_and_parser
def test_execute_args(github_ctl, parser):
    with mock.patch.object(CLIHandler, 'out') as mockingbird:
        mockingbird.return_value = True
        github_ctl.args = parser.parse_args(["dummy"])

        def test_func():
            return "output of test func"

        github_ctl.execute_arg(test_func)
        mockingbird.assert_called_once()
        mockingbird.assert_called_with("output of test func", github_ctl.args)
