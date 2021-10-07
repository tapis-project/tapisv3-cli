"""Handles TAPIS functionality related to systems."""

import json

from core.TapisController import TapisController
from tapipy.errors import InvalidInputError


class Systems(TapisController):
    """Contains all of the CRUD functions associated with systems."""
    def __init__(self):
        TapisController.__init__(self)

    def available(self, system_id) -> None:
        """Check if a system is currently enabled."""
        try:
            system = self.client.systems.isEnabled(systemId=system_id)
            status = "enabled" if system.aBool else "disabled" 
            self.logger.info(f"The system '{system_id}'' is {status}\n")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")

    def change_owner(self, system_id, username) -> None:
        """ 
        Change the owner of a system (you may lose access to a system if you
        change the owner to another user and they don't grant you permissions).
        """
        self.client.systems.changeSystemOwner(systemId=system_id, userName=username)
        self.logger.complete(f"Changed owner of system '{system_id}' to '{username}'\n")

        return

    def create(self, system_definition_file: str) -> None:
        """Create a new system from a system definition JSON file."""
        definition = json.loads(open(system_definition_file, "r").read())
        self.client.systems.createSystem(**definition)
        self.logger.success(f"System \'{definition['id']}\' created\n")

        return

    def create_user_creds(self, system_definition_file) -> None:
        """
        Create new user credentials for accessing a system. This is necessary if the
        effective user of a system is different than the owner upon system creation.
        """
        system_definition = json.loads(open(system_definition_file, "r").read())
        self.client.systems.createUserCredential(**system_definition)
        self.logger.info(f"User credentials created for user '{system_definition['userName']}'\n")
        
        return

    def delete(self, system_id) -> None:
        """
        "Soft" delete a system; it will not appear in queries. Systems are
         still present in the environment and may be undeleted.
        """
        try:
            self.client.systems.deleteSystem(systemId=system_id)
            self.logger.info(f"Deleted system with id '{system_id}'\n")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")
            return

    def disable(self, system_id) -> None:
        """Mark (all versions of) a system as unavailable for use."""
        try:
            self.client.systems.disableSystem(systemId=system_id)
            self.logger.success(f"The system '{system_id}' was disabled\n")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")   
            return       

    def enable(self, system_id) -> None:
        """Mark (all versions of) a system as available for use."""
        try:
            self.client.systems.enableSystem(systemId=system_id)
            self.logger.success(f"The system '{system_id}' was enabled\n")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")     
            return   

    def get(self, system_id) -> None:
        """Retrieve the details of an system's latest version."""
        try:
            system = self.client.systems.getSystem(systemId=system_id)
            self.logger.log(system)
            print()
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")
            return

    def getcreds(self) -> None:
        """Get a specified user's credentials."""
        # TODO
        self.logger.warn("get_credentials not implemented\n")

        return
 
    def getperms(self, system_id, username) -> None:
        """Get the permissions that a specified user has on a target system."""
        creds = self.client.systems.getUserPerms(systemId=system_id, userName=username)
        self.logger.log(creds)
        self.logger.newline(1)

        return

    def grantperms(self, system_id, username, *args) -> None:
        """Give permissions to a specified user on a target application."""
        perms = [arg.upper() for arg in args]

        # The expected input should be a JSONArray, NOT a JSONObject.
        self.client.systems.grantUserPerms(systemId=system_id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {args} granted to user '{username}'\n")
        self.logger.newline(1)

        return

    def list(self) -> None:
        """List every system in this tenant and environment."""
        systems = self.client.systems.getSystems()
        if len(systems) > 0:
            self.logger.newline(1)
            for system in systems:
                self.logger.log(system.id)
            self.logger.newline(1)
            return
        self.logger.log(f"No systems found for user '{self.client.username}'\n")

        return

    def patch(self, system_definition_file) -> None:
        """
        Update selected attributes of a system using a system definition
        JSON file containing only the required and specified attributes. 
        """
        system_definition = json.loads(open(system_definition_file, "r").read())

        if 'systemId' not in system_definition.keys():
            system_definition['systemId'] = system_definition['id']
        if 'systemVersion' not in system_definition.keys():
            system_definition['systemVersion'] = system_definition['version']

        try:
            # Update select attributes defined by the system definition file.
            self.client.systems.patchSystem(**system_definition)
            self.logger.success(f"System '{system_definition.systemId}' updated\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}\n")
            return

    def put(self, system_definition_file) -> None:
        """
        Update ALL attributes of a system using a system definition JSON
        file that contains all the same attributes used to create the system.
        """
        system_definition = json.loads(open(system_definition_file, "r").read())

        if 'systemId' not in system_definition.keys():
            system_definition['systemId'] = system_definition['id']
        if 'systemVersion' not in system_definition.keys():
            system_definition['systemVersion'] = system_definition['version']

        try:
            # Update select attributes defined by the system definition file.
            self.client.systems.putSystem(**system_definition)
            self.logger.success(f"System '{system_definition['systemId']}'' has been updated\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"Invalid Input Error: '{e.message}'\n")
            self.exit(1)

    def revokeperms(self, system_id, username, *args) -> None:
        """Revoke permissions from a specified user on a target system."""
        perms = [arg.upper() for arg in args]

        # The expected input should be a JSONArray, NOT a JSONObject.
        self.client.systems.revokeUserPerms(systemId=system_id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {perms} revoked from user '{username}'\n")

        return

    def search(self, *args) -> None:
        """
        Retrieve details for systems using attributes as search parameters.
        Multiple SQL-like queries can be done in the same set of string.
        EX: "owner = <username> AND systemType = LINUX"
        """
        matched = self.client.systems.searchSystemsRequestBody(search=args)
        for system in matched:
            print(system)
        self.logger.newline(1)

        return

    def undelete(self, system_id) -> None:
        """Undelete an applications that has been "soft" deleted."""
        try:
            self.client.systems.undeleteSystem(systemId=system_id)
            self.logger.success(f"Recovered system with id '{system_id}'\n")
            return
        except InvalidInputError:
            self.logger.info(f"Deleted system not found with id '{system_id}'\n")
            return

    def update_creds(self, file) -> None:
        """Update user credentials using a JSON definition file containing credentials."""
        creds = json.loads(open(file, "r").read())
        self.client.systems.createUserCredential(**creds)

        return