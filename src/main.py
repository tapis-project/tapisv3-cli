"""The front-controller the TAPIs command line tool."""
import sys
from core.Router import Router

def main():
    """Resolve the category, command, options, and arguments, then execute them."""
    (controller, args) = Router().resolve(sys.argv[1:])
    controller.invoke(args)
    
if __name__ == "__main__":
    main()