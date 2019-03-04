from github.cli_handler import CLIHandler
from .argparser import init_args
from .github_controller import GithubController
from .logger import logger


def main():
    try:
        logger.debug("Obtaining arguments from CLI")
        args = init_args()
        logger.debug(args)
        logger.debug("Spawning github ctl")
        github_ctl = GithubController(args)
        github_ctl()
    except Exception as e:
        # Top level handling - recoverable exceptions are handled in situ
        args = init_args()
        CLIHandler.out(str(e), args)
        exit(1)


if __name__ == '__main__':
    main()
