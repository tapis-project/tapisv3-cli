from core.Command import Command
from tapipy.errors import InvalidInputError
import json

class Files(Command):
    def __init__(self):
        Command.__init__(self)

    def create(client, system_definition_file) -> None:
        system_definition = json.loads(open(system_definition_file, "r").read())
        client.files.insert(**system_definition)

        return

    def delete(client, system_id, path) -> None:
        try:
            client.files.delete(systemId=system_id, path=path)
            print(f"Deleted file '{path}' in system '{system_id}'")
            return
        except InvalidInputError:
            print(f"File '{path}' not found in system '{system_id}'")
            return
        
    def list(self, client, system_id, path) -> None:
        files = client.files.listFiles(systemId=system_id, path=path)
        for file in files:
            print(file.name)

        return