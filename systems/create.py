from os import system
from tapipy.tapis import Tapis
import sys, json

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
system_definition_file = sys.argv[3]

client = Tapis(base_url= "https://tacc.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def create_system() -> None:
    system_definition = json.loads(open(system_definition_file, "r").read())
    client.systems.createSystem(**system_definition)

    return

if __name__ == "__main__":
    create_system()
