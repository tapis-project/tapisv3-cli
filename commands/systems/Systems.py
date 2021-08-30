from core.Command import Command
from tapipy.errors import InvalidInputError

class Systems(Command):
    def __init__(self):
        Command.__init__(self)
        self.set_option_set({
            "-f": [ "path_to_file" ],
            "-u": [ "url" ],
            "-j": [ "json" ],
            "--test": []
        })

    def list(self, client) -> None:
        systems = client.systems.getSystems()
        if len(systems) > 0:
            for system in systems:
                print(system.id)
            return

        print(f"No systems found for user 'xxx'")
        return

    def get(self, client, system_id) -> None:
        try:
            system = client.systems.getSystem(systemId=system_id)
            print(system)
            return
        except InvalidInputError:
            print(f"Sytem not found with id '{system_id}'")