from tapipy.tapis import Tapis
import sys

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
system_id = sys.argv[3]
path = sys.argv[4] if len(sys.argv) > 4 else "/"

# Authenticate
client = Tapis(base_url= "https://tacc.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def list_files() -> None:
    files = client.files.listFiles(systemId=system_id, path=path)
    for file in files:
        print(file.name)

if __name__ == "__main__":
    list_files()
