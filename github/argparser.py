from argparse import ArgumentParser

arg_parser = ArgumentParser()

arg_parser.add_argument("action",
                        nargs="+",
                        help="Github action")
arg_parser.add_argument("--url_only",
                        help="Show only url (where applicable)",
                        action="store_true",
                        )
arg_parser.add_argument("--both_urls",
                        help="Show both urls (where applicable)",
                        action="store_true"
                        )
arg_parser.add_argument("--https",
                        help="Show HTTPS URL instead of SSH",
                        action="store_true")
arg_parser.add_argument("--no_numbers",
                        help="Disables number printing in lists",
                        action="store_true")
arg_parser.add_argument("--description",
                        nargs=1,
                        type=str,
                        help="Repository description")
arg_parser.add_argument("--private",
                        action="store_true",
                        help="Create repository as private",
                        default=False)


def init_args():
    return arg_parser.parse_args()
