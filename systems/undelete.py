from tapipy.tapis import Tapis
from tapipy.errors import InvalidInputError
import sys

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
system_id = sys.argv[3]

# Authenticate
client = Tapis(base_url= "https://tacc.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def undelete_system() -> None:
    try:
        client.systems.undeleteSystem(systemId=system_id)
        print(f"Recovered system with id '{system_id}'")
        return
    except InvalidInputError:
        print(f"Deleted system not found with id '{system_id}'")
        return

if __name__ == "__main__":
    undelete_system()
