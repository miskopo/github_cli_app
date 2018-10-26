from argparse import ArgumentParser

arg_parser = ArgumentParser()

arg_parser.add_argument("action",
                        nargs="+",
                        help="Github action")
arg_parser.add_argument("--url_only",
                        help="Show only url (where applicable)",
                        action="store_true"
                        )
arg_parser.add_argument("--https",
                        help="Show HTTPS URL instead of SSH",
                        action="store_true")


def init_args():
    return arg_parser.parse_args()
