from tapipy.errors import InvalidInputError
import sys, json

def update(client, definition_file) -> None:
    app_definition = json.loads(open(definition_file, "r").read())

    try:
        # Update select attributes defined by the system definition file.
        client.apps.patchApp(**app_definition)
        return
    except InvalidInputError as e:
        print(f"Invalid Input Error: '{e.message}'")
    except:
        e = sys.exc_info()[0]
        print( f"Error: {e}" )
