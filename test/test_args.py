from pytest import raises

from github.__main__ import main


def test_no_args(capsys):
    with raises(SystemExit):
        main()


