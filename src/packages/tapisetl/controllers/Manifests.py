import json
import sys

from tapipy.errors import InvalidInputError

from packages.tapisetl.ETLController import ETLController
from core.AuthCredential import AuthCredential as Auth
from packages.tapisetl.controllers import Index
from utils.Prompt import prompt


class Manifests(ETLController):
    """Contains all of the CRUD functions associated with applications."""
    def __init__(self):
        ETLController.__init__(self)
        
    def generate_Action(self, data_system_id, data_path, manifest_system_id) -> None:
        """Check if a system is currently enabled."""
        try:
            system = self.client.systems.isEnabled(systemId=data_system_id)
            status = "enabled" if system.aBool else "disabled"
            self.logger.info(f"The system '{data_system_id}' is {status}\n")
        except InvalidInputError:
            self.logger.error(f"System not found with id '{data_system_id}'\n")
        
        """Check if data_path is good"""
        if status == "enabled":
            try:
                local_inbox = self.client.files.listFiles(systemId=data_system_id, path=data_path)
                self.logger.info(f"The files for '{data_system_id}' are: \n") 
                for file in local_inbox: print(file)
            except Exception as e:
                self.logger.error(f"Error fetching files for '{data_system_id}': {e}\n")
        
        """Check if the manifest system is available"""
        try:
            manifest_system = self.client.systems.isEnabled(systemId=manifest_system_id)
            manifest_status = "enabled" if manifest_system.aBool else "disabled"
            self.logger.info(f"The system '{manifest_system_id}' is {manifest_status}\n")
        except InvalidInputError:
            self.logger.error(f"System not found with id '{manifest_system_id}'\n")
        # """Check if the local path is available"""
        
        
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