import json
import sys

from tapipy.errors import InvalidInputError, ServerDownError, NotFoundError

from packages.tapisetl.ETLController import ETLController
from core.AuthCredential import AuthCredential as Auth

class Manifests(ETLController):
    """Contains all of the CRUD functions associated with applications."""
    def __init__(self):
        ETLController.__init__(self)

    def before(self):
        try:
            self.client = Auth().authenticate()
            if self.client is None:
                self.exit(1)
        except SystemExit:
            self.exit(1)
        except:
            raise ValueError(f"Unable to authenticate user")
        
    def validateDataSystemId_Action(self, data_system_id):
        """data_system_id(remote outbox)"""
        try:
            system= self.client.systems.isEnabled(systemId=data_system_id)
            print("hello world.")
        except:
            pass
    
    def validateDataPath_Action(self, data_path):
        """data_path(local inbox)"""
        pass
    
    def validateManifestSystemId_Action(self, manifest_system_id):
        """manifest_system_id(local outbox)"""
        pass
    
    def validateManifestPath_Action(self, manifest_path):
        """manifst_path(remote inbox)"""
        pass

    def generate_Action(self, data_system_id, data_path, manifest_system_id, manifest_path) -> None:
        #data_system_id (remote outbox) 
        
        #data_path (local inbox)
        
        #manifest_system_id (local outbox)
        
        #manifst_path (remote inbox)
        return "this is the ETL Manifest"

