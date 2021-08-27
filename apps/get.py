from tapipy.tapis import Tapis
from tapipy.errors import InvalidInputError
import sys

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
app_id = sys.argv[3]

# Authenticate
client = Tapis(base_url= "https://tacc.develop.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def get_app_by_id() -> None:
    try:
        app = client.apps.getApp(appId=app_id)
        print(app)
        return
    except InvalidInputError:
        print(f"App not found with id '{app_id}'")

if __name__ == "__main__":
    get_app_by_id()