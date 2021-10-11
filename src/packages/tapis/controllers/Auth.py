import os

from core.Controller import Controller
from core.ConfigManager import ConfigManager
from utils.Prompt import prompt
import conf.settings as settings


class Auth(Controller):
    """Configurations are parsed here."""
    def __init__(self):
        Controller.__init__(self)
        self.config = ConfigManager()

    def configure(self):
        """
        Checks if the users credentials exist for the current authentication method 
        set in the settings.py file. If it doesn't, the user will be prompted to 
        provide the credentials for the defined authentication method.
        """
        # If the configs.ini specified in the settings does not exist,
        # create it.
        if not os.path.isfile(settings.CONFIG_FILE):
            self.logger.log(f"Creating config file '{settings.CONFIG_FILE}'\n")
            self.config.create_config_file()

        # Create the credentials section if it doesn't exsit. (It's possible 
        # that the credentials section has been erased even though
        # the file exists)
        if not self.config.has_section("credentials"):
            self.config.add_section("credentials")
        

        # Add the credentials from the config 
        # file to this Configuration object's credentials dict
        for key in self.config.credentials:
            self.credentials[key] = self.parser["credentials"][key]

        # If the AUTH_METHOD doesn't have one of the values in AUTH_METHODS,
        # notify the user there is an error in the settings.py file.
        if settings.AUTH_METHOD not in settings.AUTH_METHODS:
            raise ValueError(f"Misconfigured settings.py. The AUTH_METHOD provided does not exist in the list AUTH_METHODS. AUTH_METHODS={settings.AUTH_METHODS}\n")

        # Check the current authentication method and prompt the user to provide
        # the appropriate credentials if they do not exist.
        if settings.AUTH_METHOD == settings.PASSWORD:

            # Fetch the username and password from the configs.ini if
            # they exist.
            username = None if not hasattr(self.config.credentials, "username") else self.config.credentials["username"]
            password = None if not hasattr(self.config.credentials, "password") else self.config.credentials["password"]

            # If username and password exist, return nothing.
            if bool(username) and bool(password):
                return

            # Prompt user for username and password
            self.logger.log("\nTACC credentials not found.\nProvide TACC username and password.\n")
            prompt.yes_no("Continue? [y/n]: ")

            # Prompt the username to create a username and password
            username = prompt.not_none("Username: ")
            password = prompt.not_none("Password 🔒: ", secret=True)

            # Save the credentials
            self.config.add("credentials", "username", username)
            self.config.add("credentials", "password", password)

            # Set the username and password in the Configuration's credientials dict
            self.config.credentials = {"username": username, "password": password}

            return

        # The user has misconfigured their settings.py. Let them know.
        else:
            raise ValueError(f"AUTH_METHOD provided in the settings.py is invalid. Available AUTH_METHODS: {settings.AUTH_METHODS}\n")
