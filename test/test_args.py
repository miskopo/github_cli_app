from github.__main__ import main
from pytest import raises


def set_up():
    # TODO: Install github package
    pass


def test_no_args(capsys):
    with raises(SystemExit):
        main()


