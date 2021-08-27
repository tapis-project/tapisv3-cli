from tapipy.tapis import Tapis
import sys, json

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
system_id = sys.argv[3]
file_path = sys.argv[4]

client = Tapis(base_url= "https://tacc.develop.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def create_system() -> None:
    system_definition = json.loads(open(system_definition_file, "r").read())
    client.files.insert(**system_definition)

    return

if __name__ == "__main__":
    create_system()