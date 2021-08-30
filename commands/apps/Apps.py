import json, sys, inspect

from core.Command import Command
from tapipy.errors import InvalidInputError, ServerDownError

class Apps(Command):
    def __init__(self):
        Command.__init__(self)
        self.set_option_set({
            "-f": [ "path_to_file" ],
            "-u": [ "url" ],
            "-j": [ "json" ],
            "--test": []
        })

    def create(self, client, definition_file) -> None:
        try:
            definition = json.loads(open(definition_file, "r").read())
            client.apps.createAppVersion(**definition)
            return
        except ServerDownError as e:
            print(e)         

    def delete(self, client, id) -> None:
        try:
            client.apps.deleteApp(appId=id)
            print(f"Deleted app with id '{id}'")
            return
        except InvalidInputError:
            print(f"App not found with id '{id}'")
            return

    def get(self, client, id, version) -> None:
        try:
            app = client.apps.getApp(appId=id, appVersion=version)
            print(app)
            return
        except InvalidInputError as e:
            print(f"{e.message}")

    def list(self, client) -> None:
        apps = client.apps.getApps()
        if len(apps) > 0:
            for app in apps:
                print(app.id)
            return

        print(f"No apps found for user '{client.username}'")
        return

    def undelete(self, client, id) -> None:
        try:
            client.apps.undeleteApp(appId=id)
            print(f"Recovered app with id '{id}'")
            return
        except InvalidInputError:
            print(f"Deleted app not found with id '{id}'")
            return

    def update(self, client, definition_file) -> None:
        app_definition = json.loads(open(definition_file, "r").read())

        try:
            # Update select attributes defined by the system definition file.
            client.apps.patchApp(**app_definition)
            return
        except InvalidInputError as e:
            print(f"Invalid Input Error: '{e.message}'")
        except:
            e = sys.exc_info()[0]
            print( f"Error: {e}" )