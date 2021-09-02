from core.TapisCommand import TapisCommand
from tapipy.errors import InvalidInputError
import json, sys

class Systems(TapisCommand):
    def __init__(self):
        TapisCommand.__init__(self)
        self.set_option_set({
            "-f": [ "path_to_file" ],
            "-u": [ "url" ],
            "-j": [ "json" ],
            "--test": []
        })

    def change_owner(self, client, system_id, username):
        client.systems.changeSystemOwner(systemId=system_id, userName=username)
        
        return

    def create(self, client, definition_file: str) -> None:
        system_definition = json.loads(open(definition_file, "r").read())
        client.systems.createSystem(**system_definition)

        return

    def create_user_creds(self, client, system_definition_file) -> None:
        system_definition = json.loads(open(system_definition_file, "r").read())
        client.systems.createUserCredential(**system_definition)

        return

    def delete(self, client, system_id) -> None:
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
            print(f"System not found with id '{system_id}'")

    def get_credentials(self, client):
            self.logger.warn("get_credentials not implemented")

    def get_permissions(self, client, system_id, username):
            creds = client.systems.getUserPerms(systemId=system_id, userName=username)
            self.logger.log(creds)
            return

    def list(self, client) -> None:
        systems = client.systems.getSystems()
        if len(systems) > 0:
            for system in systems:
                print(system.id)
            return

        print(f"No systems found for user '{client.username}'")
        return

    def undelete(self, client, system_id) -> None:
        try:
            client.systems.undeleteSystem(systemId=system_id)
            print(f"Recovered system with id '{system_id}'")
            return
        except InvalidInputError:
            print(f"Deleted system not found with id '{system_id}'")
            return

    def update(self, client, system_definition_file) -> None:
        system_definition = json.loads(open(system_definition_file, "r").read())

        try:
            # Update select attributes defined by the system definition file.
            client.systems.patchSystem(**system_definition)
            return
        except InvalidInputError as e:
            print(f"Invalid Input Error: '{e.message}'")
        except:
            e = sys.exc_info()[0]
            self.logger.error( f"{e}" )

    def update_creds(self, client, credentials_file):
        print(client.systems)
        client.systems.createUserCredential(credentials_file)