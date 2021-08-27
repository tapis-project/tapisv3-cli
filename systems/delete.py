from tapipy.tapis import Tapis
from tapipy.errors import InvalidInputError
import sys

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
system_id = sys.argv[3]

# Authenticate
client = Tapis(base_url= "https://tacc.develop.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def delete_system() -> None:
    try:
        client.systems.deleteSystem(systemId=system_id)
        print(f"Deleted system with id '{system_id}'")
        return
    except InvalidInputError:
        print(f"System not found with id '{system_id}'")
        return

if __name__ == "__main__":
    delete_system()
