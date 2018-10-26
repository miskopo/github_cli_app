from .github_controller import GithubController
from .logger import logger
from .argparser import init_args


def main():
    logger.debug("Obtaining arguments from CLI")
    args = init_args()
    logger.debug(args)
    logger.debug("Spawning github ctl")
    github_ctl = GithubController(args)
    github_ctl()


if __name__ == '__main__':
    main()
