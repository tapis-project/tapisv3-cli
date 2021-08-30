from core.Command import Command
from tapipy.errors import InvalidInputError
import json, sys

class Systems(Command):
    def __init__(self):
        Command.__init__(self)
        self.set_option_set({
            "-f": [ "path_to_file" ],
            "-u": [ "url" ],
            "-j": [ "json" ],
            "--test": []
        })

    def create(client, system_definition_file) -> None:
        system_definition = json.loads(open(system_definition_file, "r").read())
        client.systems.createSystem(**system_definition)

        return

    def delete(client, system_id) -> None:
        try:
            client.systems.deleteSystem(systemId=system_id)
            print(f"Deleted system with id '{system_id}'")
            return
        except InvalidInputError:
            print(f"System not found with id '{system_id}'")
            return

    def get(self, client, system_id) -> None:
        try:
            system = client.systems.getSystem(systemId=system_id)
            print(system)
            return
        except InvalidInputError:
            print(f"Sytem not found with id '{system_id}'")

    def list(self, client) -> None:
        systems = client.systems.getSystems()
        if len(systems) > 0:
            for system in systems:
                print(system.id)
            return

        print(f"No systems found for user '{client.username}")
        return

    def undelete(client, system_id) -> None:
        try:
            client.systems.undeleteSystem(systemId=system_id)
            print(f"Recovered system with id '{system_id}'")
            return
        except InvalidInputError:
<<<<<<< HEAD
            print(f"System not found with id '{system_id}'")
=======
            print(f"Deleted system not found with id '{system_id}'")
            return

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
>>>>>>> fd5e17fba5b02e5455b828ddedd9ccb54c1b669f
