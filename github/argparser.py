from argparse import ArgumentParser

arg_parser = ArgumentParser()

actions = ['register',
           'list-my-repositories',
           'list-user-repositories',
           'create-repository',
           'create-new-repository',
           'delete-repository',
           'create-project',
           'create-pull-request']

arg_parser.add_argument("action",
                        nargs=1,
                        help="Github action",
                        choices=actions)
arg_parser.add_argument("parameters",
                        nargs="*",
                        help="Parameter of specified action, e.g. username, repository name etc.")
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
                        help="Disable number printing in lists",
                        action="store_true")
arg_parser.add_argument("--description",
                        nargs=1,
                        type=str,
                        help="Repository description")
arg_parser.add_argument("--private",
                        action="store_true",
                        help="Create repository as private",
                        default=False)
arg_parser.add_argument("--no_confirm",
                        help="Disable confirmation dialogs",
                        action="store_true",
                        default=False)


def init_args():
    return arg_parser.parse_args()
