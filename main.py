from core.Authenticator import Authenticator as Auth
from core.Resolver import Resolver
import sys

def main():
    # Resolve the command, action, options, and arguments, then execute it
    (command, args) = Resolver().resolve(sys.argv[1:])
    command.execute(args)
    
if __name__ == "__main__":
    main()