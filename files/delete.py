from tapipy.tapis import Tapis
from tapipy.errors import InvalidInputError
import sys

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
system_id = sys.argv[3]
file_path = sys.argv[4]

# Authenticate
client = Tapis(base_url= "https://tacc.develop.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

print(dir(client.files))

def delete_file() -> None:
    try:
        client.files.delete(systemId=system_id, path=file_path)
        print(f"Deleted file '{file_path}' in system '{system_id}'")
        return
    except InvalidInputError:
        print(f"File '{file_path}' not found in system '{system_id}'")
        return

if __name__ == "__main__":
    delete_file()