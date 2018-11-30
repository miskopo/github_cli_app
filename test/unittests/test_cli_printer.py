from argparse import ArgumentParser

from colorama import Fore

from github.cli_printer import CLIPrinter


def setup_arg_parser():
    parser = ArgumentParser()
    parser.add_argument("action", nargs="+")
    parser.add_argument("--both_urls", action="store_true")
    parser.add_argument("--no_numbers", action="store_true")
    parser.add_argument("--url_only", action="store_true")
    parser.add_argument("--https", action="store_true")
    parser.add_argument("--private", action="store_true")
    parser.add_argument("--description")

    return parser


def test_general_string(capsys):
    args = setup_arg_parser().parse_args(["dummy"])
    string = ""
    CLIPrinter.out(string, args)
    out, err = capsys.readouterr()
    assert not err
    assert out == "\n"

    string = "test plain string"
    CLIPrinter.out(string, args)
    out, err = capsys.readouterr()
    assert not err
    assert out == "test plain string\n"

    number = 42
    CLIPrinter.out(number, args)
    out, err = capsys.readouterr()
    assert not err
    assert out == "42\n"


def test_composed_data(capsys):
    args = setup_arg_parser().parse_args(["dummy"])
    composed_data = [('name', 'url', 'ssh_url')]
    CLIPrinter.out(composed_data, args)
    out, err = capsys.readouterr()
    assert not err
    assert out == f"{Fore.GREEN}1.{Fore.RESET}\nname\nurl\nssh_url\n"

    composed_data = [('name', 'url', 'ssh_url'), ('name2', 'url2', 'ssh_url2')]
    CLIPrinter.out(composed_data, args)
    out, err = capsys.readouterr()
    assert not err
    assert out == f"{Fore.GREEN}1.{Fore.RESET}\nname\nurl\nssh_url\n{Fore.GREEN}2.{Fore.RESET}\nname2\nurl2\nssh_url2\n"

    args = setup_arg_parser().parse_args(["dummy", "--no_numbers"])
    CLIPrinter.out(composed_data, args)
    out, err = capsys.readouterr()
    assert not err
    assert out == "name\nurl\nssh_url\nname2\nurl2\nssh_url2\n"
