"""The front-controller the TAPIS command line tool."""
import sys, readline

from core.Router import Router
from utils.Logger import logger

def run(args):
    (controller, args) = Router().resolve(args)
    try:
        controller.invoke(args)
    except Exception as e:
        logger.error(e)

def main():
    if len(sys.argv[1:]) > 0 and sys.argv[1:][0] == "shell":
        try:
            while True:
                string = input("\nt>>> ")
                if string == "exit":
                    raise KeyboardInterrupt
                args = string.split(" ") if string != "" else []
                run(args)
        except KeyboardInterrupt:
            print("Exiting tapis shell")
            return
        except SystemExit:
            main()
            return

    run(sys.argv[1:])


if __name__ == "__main__":
    main()
