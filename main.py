from core.Authenticator import Authenticator as Auth
from core.Resolver import Resolver
import sys

def main():
    client = Auth().authenticate(
        {"username": sys.argv[1], "password": sys.argv[2]},
        auth_method="PASSWORD"
    )

    # Resolve the command, action, options, and arguments, then execute it
    (command, args) = Resolver().resolve(sys.argv[3:])
    command.execute(client, args)
    
if __name__ == "__main__":
    main()