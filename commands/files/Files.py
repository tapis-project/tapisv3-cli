from core.Command import Command
from tapipy.errors import InvalidInputError

class Files(Command):
    def __init__(self):
        Command.__init__(self)
        
    def list(self, client, system_id, path) -> None:
        files = client.files.listFiles(systemId=system_id, path=path)
        for file in files:
            print(file.name)

        return