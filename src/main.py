"""The front-controller the TAPIS command line tool."""
import sys

from core.Router import Router
from utils.Logger import logger


def main():
    """Resolve the category, command, options, and arguments, and then execute them."""
    (controller, args) = Router().resolve(sys.argv[1:])
    try:
        controller.invoke(args)
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    main()
