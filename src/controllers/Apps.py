"""Handles TAPIS functionality related to applications."""

import json
import sys

from core.TapisController import TapisController
from tapipy.errors import InvalidInputError, ServerDownError


class Apps(TapisController):
    """Contains all of the CRUD functions associated with applications."""
    def __init__(self):
        TapisController.__init__(self)

    def available(self, app_id) -> None:
        """ Check if an application is currently enabled. """
        try:
            app = self.client.apps.isEnabled(appId=app_id)
            status = "enabled" if app.aBool else "disabled"
            self.logger.info(f"The app '{app_id}' is {status}\n")
            return
        except InvalidInputError:
            self.logger.error(f"App not found with id '{app_id}'\n")
            return

    def change_owner(self, app_id, username) -> None:
        """
        Change the owner of an application (you may lose access to an app
        if you change the owner to another user and they don't grant you
        permissions).
        """
        self.client.apps.changeAppOwner(appId=app_id, userName=username)
        self.logger.complete(f"\nChanged owner of app '{app_id}' to '{username}'\n")

        return

    def create(self, app_definition_file) -> None:
        """Create a new application from an app definition JSON file."""
        try:
            definition = json.loads(open(app_definition_file, "r").read())
            self.client.apps.createAppVersion(**definition)
            self.logger.success(f"App \'{definition['id']}\' created\n")
            return
        except (ServerDownError, InvalidInputError) as e:
            self.logger.error(e)
            self.logger.newline(1)
            return

    def delete(self, app_id) -> None:
        """
        "Soft" delete an application; it will not appear in queries.
        Apps are still present in the environment and may be undeleted.
        """
        try:
            self.client.apps.deleteApp(appId=app_id)
            self.logger.info(f"Deleted app with id '{app_id}'\n")
            return
        except InvalidInputError:
            self.logger.error(f"App not found with id '{app_id}'\n")
            return

    def disable(self, app_id) -> None:
        """Mark (all versions of) an application as unavailable for use."""
        try:
            self.client.apps.disableApp(appId=app_id)
            self.logger.success(f"The app '{app_id}' was disabled\n")
            return
        except InvalidInputError:
            self.logger.error(f"App not found with id '{app_id}'\n")
            return

    def enable(self, app_id) -> None:
        """Mark (all versions of) an application as available for use."""
        try:
            self.client.apps.enableApp(appId=app_id)
            self.logger.success(f"The app '{app_id}' was enabled\n")
            return
        except InvalidInputError:
            self.logger.error(f"App not found with id '{app_id}'\n")
            return

    def get(self, app_id) -> None:
        """Retrieve the details of an application's latest version."""
        try:
            app = self.client.apps.getAppLatestVersion(appId=app_id)
            self.logger.log(app)
            self.logger.newline(1)
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}\n")
            self.exit(1)
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"{e.message}\n")
            self.exit(1)

    def getversion(self, app_id, version) -> None:
        """Retrieve the details of the specified version of an application."""
        try:
            app = self.client.apps.getApp(appId=app_id, appVersion=version)
            self.logger.log(app)
            self.logger.newline(1)
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}\n")
            self.exit(1)
        except:
            e = sys.exc_info()[0]
            self.logger.error(f"{e.message}\n")
            self.exit(1)

    def getperms(self, app_id, username) -> None:
        """Get the permissions that a specified user has on a target application."""
        creds = self.client.apps.getUserPerms(appId=app_id, userName=username)
        self.logger.log(creds)
        self.logger.newline(1)

        return

    def grantperms(self, app_id, username, *args) -> None:
        """Give permissions to a specified user on a target application."""
        perms = [arg.upper() for arg in args]

        # The expected input should be a JSONArray, NOT a JSONObject.
        self.client.apps.grantUserPerms(appId=app_id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {perms} granted to user '{username}'\n")

        return

    def list(self) -> None:
        """List every application on the systems in this tenant and environment."""
        apps = self.client.apps.getApps()
        if len(apps) > 0:
            self.logger.newline(1)
            for app in apps:
                self.logger.log(app.id)
            self.logger.newline(1)
            return

        self.logger.log(f"No apps found for user '{self.client.username}'\n")
        return

    def patch(self, app_definition_file) -> None:
        """
        Update selected attributes of an application using an app definition
        JSON file containing only the required and specified attributes.
        """
        app_definition = json.loads(open(app_definition_file, "r").read())

        if 'appId' not in app_definition.keys():
            app_definition['appId'] = app_definition['id']
        if 'appVersion' not in app_definition.keys():
            app_definition['appVersion'] = app_definition['version']

        try:
            # Update select attributes defined by the system definition file.
            self.client.apps.patchApp(**app_definition)
            self.logger.success(f"App '{app_definition['appId']}' has been updated\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"Invalid Input Error: '{e.message}'\n")
            self.exit(1)
        except:
            e = sys.exc_info()[0]
            self.logger.error( f"{e}\n" )
            self.exit(1)

    def put(self, app_definition_file) -> None:
        """
        Update ALL attributes of an application using an app definition JSON
        file that contains all the same attributes used to create the app.
        """
        app_definition = json.loads(open(app_definition_file, "r").read())

        if 'appId' not in app_definition.keys():
            app_definition['appId'] = app_definition['id']
        if 'appVersion' not in app_definition.keys():
            app_definition['appVersion'] = app_definition['version']

        try:
            # Update select attributes defined by the system definition file.
            self.client.apps.putApp(**app_definition)
            self.logger.success(f"App '{app_definition['appId']}' has been updated\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"Invalid Input Error: '{e.message}'\n")
            self.exit(1)
        except:
            e = sys.exc_info()[0]
            self.logger.error( f"{e}\n" )
            self.exit(1)

    def revokeperms(self, app_id, username, *args) -> None:
        """Revoke permissions from a specified user on a target application."""
        perms = [arg.upper() for arg in args]

        # The expected input should be a JSONArray, NOT a JSONObject.
        self.client.apps.revokeUserPerms(appId=app_id, userName=username, permissions=perms)
        self.logger.info(f"Permissions {perms} revoked from user '{username}'\n")

        return

    def search(self, *args) -> None:
        """
        Retrieve details for applications using attributes as search parameters.
        Multiple SQL-like queries can be done in the same set of string.
        EX: "owner = <username> AND systemType = LINUX"
        """
        matched = self.client.apps.searchAppsRequestBody(search=args)
        for app in matched:
            print(app)
        self.logger.newline(1)

        return

    def undelete(self, app_id) -> None:
        """Undelete an applications that has been "soft" deleted."""
        try:
            self.client.apps.undeleteApp(appId=app_id)
            self.logger.success(f"Recovered app with id '{app_id}'\n")
            return
        except InvalidInputError:
            self.logger.error(f"Deleted app not found with id '{app_id}'\n")
            return
