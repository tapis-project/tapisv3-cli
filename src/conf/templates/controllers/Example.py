import json

from tapipy.errors import InvalidInputError

from packages.tapis.TapisController import TapisController


# This example controller queries and mutates the tapis Systems API
class Example(TapisController):
    # Tapis controller abstracts away client initialization and authentication.
    # Make calls with the tapis client using self.client
    def __init__(self):
        TapisController.__init__(self)

    # All methods called that are suffixed with the ACTION_FILTER_SUFFIX(_Action by default)
    # will run 3 methods. First it calls BaseClass.before(), then itself,
    # then BaseClass.after(). Before and after filters are available
    # on all controllers that inherit the BaseClass class. By default, they're before
    # and after do nothing. You may define your own before and after methods on 
    # controller classes.
    def available_Action(self, system_id) -> None:
        """Check if a system is currently enabled."""
        try:
            system = self.client.systems.isEnabled(systemId=system_id)
            status = "enabled" if system.aBool else "disabled"
            self.logger.info(f"The system '{system_id}' is {status}\n")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")

    def change_owner_Action(self, system_id, username) -> None:
        self.client.systems.changeSystemOwner(systemId=system_id, userName=username)
        self.logger.complete(f"Changed owner of system '{system_id}' to '{username}'\n")

        return

    def create_Action(self, system_definition_file: str) -> None:
        definition = json.loads(open(system_definition_file, "r").read())
        self.client.systems.createSystem(**definition)
        self.logger.success(f"System \'{definition['id']}\' created\n")

        return

    def create_user_creds_Action(self, system_definition_file) -> None:
        system_definition = json.loads(open(system_definition_file, "r").read())
        self.client.systems.createUserCredential(**system_definition)
        self.logger.info(f"User credentials created for user '{system_definition['userName']}'\n")

        return

    def delete_Action(self, system_id) -> None:
        try:
            self.client.systems.deleteSystem(systemId=system_id)
            self.logger.info(f"Deleted system with id '{system_id}'\n")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")
            return

    def disable_Action(self, system_id) -> None:
        try:
            self.client.systems.disableSystem(systemId=system_id)
            self.logger.success(f"The system '{system_id}' was disabled\n")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")
            return

    def enable_Action(self, system_id) -> None:
        try:
            self.client.systems.enableSystem(systemId=system_id)
            self.logger.success(f"The system '{system_id}' was enabled\n")
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")
            return

    def get_Action(self, system_id) -> None:
        try:
            system = self.client.systems.getSystem(systemId=system_id)
            self.logger.log(system)
            print()
            return
        except InvalidInputError:
            self.logger.error(f"System not found with id '{system_id}'\n")
            return

    def getperms_Action(self, system_id, username) -> None:
        creds = self.client.systems.getUserPerms(systemId=system_id, userName=username)
        self.logger.log(creds)
        self.logger.newline(1)

        return

    def grantperms_Action(self, system_id, username, *args) -> None:
        perms = [arg.upper() for arg in args]
        self.client.systems.grantUserPerms(systemId=system_id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {args} granted to user '{username}'\n")
        self.logger.newline(1)

        return

    def list_Action(self) -> None:
        systems = self.client.systems.getSystems()
        if len(systems) > 0:
            self.logger.newline(1)
            for system in systems:
                self.logger.log(system.id)
            self.logger.newline(1)
            return
        self.logger.log(f"No systems found for user '{self.client.username}'\n")

        return

    def patch_Action(self, system_definition_file) -> None:
        try:
            system_definition = json.loads(open(system_definition_file, "r").read())
        except FileNotFoundError as e:
            self.logger.error(e)
            self.exit(1)

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

    def put_Action(self, system_definition_file) -> None:
        try:
            system_definition = json.loads(open(system_definition_file, "r").read())
        except FileNotFoundError as e:
            self.logger.error(e)
            self.exit(1)

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

    def revokeperms_Action(self, system_id, username, *args) -> None:
        perms = [arg.upper() for arg in args]

        # The expected input should be a JSONArray, NOT a JSONObject.
        self.client.systems.revokeUserPerms(systemId=system_id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {perms} revoked from user '{username}'\n")

        return

    def search_Action(self, *args) -> None:
        matched = self.client.systems.searchSystemsRequestBody(search=args)
        for system in matched:
            print(system)
        self.logger.newline(1)

        return

    def undelete_Action(self, system_id) -> None:
        try:
            self.client.systems.undeleteSystem(systemId=system_id)
            self.logger.success(f"Recovered system with id '{system_id}'\n")
            return
        except InvalidInputError:
            self.logger.info(f"Deleted system not found with id '{system_id}'\n")
            return

    def update_creds_Action(self, file) -> None:
        creds = json.loads(open(file, "r").read())
        self.client.systems.createUserCredential(**creds)

        return