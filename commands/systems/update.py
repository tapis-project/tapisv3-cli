from tapipy.errors import InvalidInputError
import sys, json

def update(client, system_definition_file) -> None:
    system_definition = json.loads(open(system_definition_file, "r").read())

    try:
        # Update select attributes defined by the system definition file.
        client.systems.patchSystem(**system_definition)
        return
    except InvalidInputError as e:
        print(f"Invalid Input Error: '{e.message}'")
    except:
        e = sys.exc_info()[0]
        print( f"Error: {e}" )
