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
    except KeyboardInterrupt:
        CLIHandler.out("Interrupted by user. Exiting.", None)
        exit(1)
    except Exception as e:
        # Top level handling - recoverable exceptions are handled inplace
        CLIHandler.out(str(e), None)
        exit(1)


if __name__ == '__main__':
    main()
