import json

from tapipy.errors import InvalidInputError

from packages.tapisetl.ETLController import ETLController
from tapisetl.controllers.Index import Index

print("this is the Datavalidators")

class DataValidator(ETLController):
    """Contains all of the CRUD functions associated with systems."""
    def __init__(self):
        Index.__init__(self)

        print("this is from the DataValidator")

    def remoteOutboxAvailable_Action(self, remoteOut) -> None:
        """Check if the remote outbox is currently enabled."""
            
    def localInboxAvailable_Action(self, localIn) -> None:
        """Check if the local inbox is available."""    
            
    def localOutboxAvailable_Action(self, localOut) -> None:
        """Check if the local outbox is available."""
    def RemoteInboxAvailable_Action(self, RemoteIn) -> None:
        """Check if the remote outbox is available."""
        
DvD_instance = DataValidator()
print(DataValidator())