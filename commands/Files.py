from core.TapisCommand import TapisCommand
from tapipy.errors import InvalidInputError
import json

class Files(TapisCommand):
    def __init__(self):
        TapisCommand.__init__(self)

    def create(self, system_definition_file) -> None:
        system_definition = json.loads(open(system_definition_file, "r").read())
        self.client.files.insert(**system_definition)

        return

    def delete(self, system_id, path) -> None:
        try:
            self.client.files.delete(systemId=system_id, path=path)
            print(f"Deleted file '{path}' in system '{system_id}'")
            return
        except InvalidInputError:
            print(f"File '{path}' not found in system '{system_id}'")
            return

    def get_contents(self, system_id, path) -> None:
        print(dir(self.client.files.getContents))
        try:
            self.client.files.getConents(systemId=system_id, path=path)
            self.logger.complete(f"Fetched contents of file {path} fetched")
            return
        except InvalidInputError:
            print(f"File '{path}' not found in system '{system_id}'")
            return

        
    def list(self, system_id, path) -> None:
        files = self.client.files.listFiles(systemId=system_id, path=path)
        for file in files:
            print(file.name)

        return

    # Destination must inlcude all sub directories and a filename
    # Directories that don't exist in destination will be created
    def upload(self, system_id, path_to_file, destination) -> None:    
        # NOTE Tapipy client hasn't yet implemented the insert method in
        # the files module. The function upload on the Tapis class handles
        # this instead.
        try:
            self.client.upload(
                system_id = system_id,
                source_file_path = path_to_file,
                dest_file_path = destination
            )
            
        except Exception as e:
            self.logger.error(e.message)
            self.exit(1)