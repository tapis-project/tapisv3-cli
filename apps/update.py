from tapipy.tapis import Tapis
from tapipy.errors import InvalidInputError
import sys, json

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
app_definition_file = sys.argv[3]

# Authenticate
client = Tapis(base_url= "https://tacc.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def update_app() -> None:
    app_definition = json.loads(open(app_definition_file, "r").read())

    try:
        # Update select attributes defined by the system definition file.
        client.apps.patchApp(**app_definition)
        return
    except InvalidInputError as e:
        print(f"Invalid Input Error: '{e.message}'")
    except:
        e = sys.exc_info()[0]
        print( f"Error: {e}" )
        

if __name__ == "__main__":
    update_app()
