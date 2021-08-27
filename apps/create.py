from tapipy.tapis import Tapis
from tapipy.errors import InvalidInputError
import sys, json

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
app_definition_file = sys.argv[3]

client = Tapis(base_url= "https://tacc.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

# print(dir(client.apps))

def create_app() -> None:
    app_definition = json.loads(open(app_definition_file, "r").read())
    client.apps.createApp(**app_definition)

#     return

if __name__ == "__main__":
    create_app()