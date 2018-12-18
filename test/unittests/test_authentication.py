import builtins
from os import environ, remove
from os.path import dirname, exists
from shutil import copyfile, move
from unittest import mock

from pytest import raises

import github
from github.authentication import load_api_key, register_api_key
from github.common import InvalidAPIKeyException


def backup_and_restore_api_file(func):
    def inner():
        if exists(f'{dirname(github.__file__)}/../api_key'):
            copyfile(f'{dirname(github.__file__)}/../api_key', f'{dirname(github.__file__)}/../api_key_bcp')
        try:
            func()
        finally:
            remove(f'{dirname(github.__file__)}/../api_key')
            if exists(f'{dirname(github.__file__)}/../api_key_bcp'):
                move(f'{dirname(github.__file__)}/../api_key_bcp', f'{dirname(github.__file__)}/../api_key')
    return inner


def backup_and_restore_env_var(func):
    def inner():
        try:
            key_bcp = environ['GITHUB_API_KEY']
        except KeyError:
            func()
        else:
            del environ['GITHUB_API_KEY']
            func()
            environ['GITHUB_API_KEY'] = key_bcp
    return inner


def test_load_api_key_from_environ():
    api_key = '1234567890123456789012345678901234567890'
    with mock.patch.dict(environ, {'GITHUB_API_KEY': api_key}):
        assert load_api_key() == api_key

    api_key = 'not_long_enough'
    with mock.patch.dict(environ, {'GITHUB_API_KEY': api_key}):
        with raises(InvalidAPIKeyException):
            load_api_key()


@backup_and_restore_env_var
@backup_and_restore_api_file
def test_load_api_key_from_file():
    with open(f'{dirname(github.__file__)}/../api_key', "w") as key_file:
        api_key = '1234567890123456789012345678901234567890'
        key_file.write(api_key)
    assert load_api_key() == api_key

    with open(f'{dirname(github.__file__)}/../api_key', "w") as key_file:
        api_key = 'not_long_enough'
        key_file.write(api_key)
    with raises(InvalidAPIKeyException):
        load_api_key()


def test_register_api_key():
    api_key = '1234567890123456789012345678901234567890'
    with mock.patch.dict(environ, {'GITHUB_API_KEY': api_key}):
        with mock.patch.object(builtins, 'input', lambda _: '1'):
            assert register_api_key() == "Using already registered API KEY"

        with mock.patch.object(builtins, 'input', lambda _: 'NONSENSE'):
            assert register_api_key() == "Maximum attempts provided, exiting"
