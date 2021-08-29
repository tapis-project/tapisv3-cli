from core.Authenticator import Authenticator as Auth
from core.CommandResolver import CommandResolver as Resolver
import sys

def init():
    client = Auth().authenticate(
        {"username": sys.argv[1], "password": sys.argv[2]},
        auth_method="PASSWORD"
    )

    command = Resolver().resolve(sys.argv[3:])
    command(client)
    

if __name__ == "__main__":
    init()