from tapipy.tapis import Tapis
from tapipy.errors import InvalidInputError
import sys

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
system_id = sys.argv[3]

# Authenticate
client = Tapis(base_url= "https://tacc.develop.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def get_system_by_id() -> None:
    try:
        system = client.systems.getSystem(systemId=system_id)
        print(system)
        return
    except InvalidInputError:
        print(f"Sytem not found with id '{system_id}'")

if __name__ == "__main__":
    get_system_by_id()