import json, time, uuid, os

from tapipy.errors import InvalidInputError

from packages.tapisetl.ETLController import ETLController
from core.AuthCredential import AuthCredential as Auth
from packages.tapisetl.controllers import Index
from utils.Prompt import prompt


class Manifests(ETLController):
    """Contains all of the CRUD functions associated with applications."""
    def __init__(self):
        ETLController.__init__(self)
      
    def generate_Action(
            self,
            data_system_id: str,
            data_path: str,
            manifest_system_id: str,
            manifest_path: str,
            *file_names_to_track: tuple[str]
        ) -> None:
        # Fetch all of the files on the data system at the data path
        try:
            all_data_files = self.client.files.listFiles(systemId=data_system_id, path=data_path)
        except Exception as e:
            self.logger.error(f"Error fetching files for '{data_system_id}': {e}\n")
        
        # Get the file objects that correspond to the names provided in
        # file_names_to_track
        data_files = []
        for file in all_data_files:
            if file.name in file_names_to_track:
                data_files.append(file)

        # Determine invalid files
        invalid_data_files = []
        data_file_names = [f.name for f in data_files]
        for file_name_to_track in file_names_to_track:
            if file_name_to_track not in data_file_names:
                invalid_data_files.append(file_name_to_track)

        # Raise Exception if user provides invalid file names (names of files that
        # do not exist)
        if len(invalid_data_files) > 0:
            raise Exception(f"Invalid data file name(s) provided: {invalid_data_files}")

        created_at = time.time()
        new_manifest = {
            "status": "pending",
            "phase": "ingress",
            "local_files": [],
            "transfers": [],
            "remote_files": [data_file.__dict__ for data_file in data_files],
            "jobs": [],
            "logs": [f"{created_at} Created"],
            "created_at": created_at,
            "last_modified": created_at,
            "metadata": {}
        }
        
        
        manifest_file_name = f"{str(uuid.uuid4())}.json"
        try:
            new_manifest_path = os.path.join(manifest_path, manifest_file_name)
            self.client.files.insert(
                systemId=manifest_system_id,
                path=new_manifest_path,
                file=json.dumps(new_manifest)
            )
            self.logger.complete(f"Created manifest '{manifest_file_name}' on system '{manifest_system_id}' | Path: {new_manifest_path}")
        except Exception as e:
            self.logger.error(f"Error writing: '{file}' to '{new_manifest_path}': {e}")
       
"""
    def manifestPrompt(self, *_, **__):
        #Prompt user for data ingress and egress
        
        data_system_id = prompt.text("Data system Id?")
        localInbox = prompt.text("Where is the localInbox?")

        self.directories = {'remoteOutbox': data_system_id, 
                            'localInbox': localInbox, 
                            }
        
        self.generate_Action(data_system_id=data_system_id)
        return self.directories
"""

newManifest = Manifests()