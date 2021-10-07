"""Handles the setup of authorization credentials."""

import os
import sys

from configs import settings
from configparser import ConfigParser
from getpass import getpass
from utils.Logger import Logger


class Configuration:
    """
    Writes user credentials to the configs.ini based on the AUTH_METHOD 
    provided in the settings.py file.
    """
    auth_method: str = settings.AUTH_METHOD
    config: ConfigParser = None
    credentials: dict = {}

    def __init__(self):
        # Intialize and set the configparser to the Configuration object and
        # get the credentials from the config file.
        self.config = ConfigParser()
        self.config.read(settings.CONFIG_FILE)
        self.logger = Logger()

        # Add the credentials from the config file to 
        # this Configuration object's credentials dict.
        if "credentials" in self.config.sections():
            for key in self.config["credentials"]:
                self.credentials[key] = self.config["credentials"][key]

    def configure(self) -> None:
        """
        Checks if the users credentials exist for the current authentication method 
        set in the settings.py file. If it doesn't, the user will be prompted to 
        provide the credentials for the defined authentication method.
        """
        # If the configs.ini specified in the settings does not exist,
        # create it.
        if not os.path.isfile(settings.CONFIG_FILE):
            print(f"Creating config file '{settings.CONFIG_FILE}'\n")
            self.config["credentials"] = {}
            with open(settings.CONFIG_FILE, "w") as file:
                self.config.write(file)

        # Create the credentials section if it doesn't exsit. (It's possible 
        # that the credentials section has been erased even though
        # the file exists) 
        if "credentials" not in self.config.sections():
            self.config["credentials"] = {}
            with open(settings.CONFIG_FILE, "w") as file:
                self.config.write(file)

        # Add the credentials from the config 
        # file to this Configuration object's credentials dict
        for key in self.config["credentials"]:
            self.credentials[key] = self.config["credentials"][key]

        # If the AUTH_METHOD doesn't have one of the values in AUTH_METHODS,
        # notify the user there is an error in the settings.py file.
        if settings.AUTH_METHOD not in settings.AUTH_METHODS:
            raise ValueError(f"Misconfigured settings.py. The AUTH_METHOD provided does not exist in the list AUTH_METHODS. AUTH_METHODS={settings.AUTH_METHODS}\n")

        # Check the current authentication method and prompt the user to provide
        # the appropriate credentials if they do not exist.
        if settings.AUTH_METHOD == settings.PASSWORD:

            # Fetch the username and password from the configs.ini if
            # they exist.
            username = None if not hasattr(self.config["credentials"], "username") else self.config["credentials"]["username"]
            password = None if not hasattr(self.config["credentials"], "password") else self.config["credentials"]["password"]

            # If username and password exist, return nothing.
            if bool(username) and bool(password):
                return

            # Prompt user for username and password
            print("\nTACC credentials not found.\nProvide TACC username and password.\n")
            
            self.prompt_yes_no_exit("Continue? [y/n]: ")

            # Prompt the username to create a username and password
            username = self.prompt_not_none("Username: ")
            password = self.prompt_not_none("Password 🔒: ", secret=True)

            # Save the credentials
            self.config["credentials"]["username"] = username
            self.config["credentials"]["password"] = password

            with open(settings.CONFIG_FILE, "w") as file:
                self.config.write(file)

            # Set the username and password in the Configuration's credientials dict
            self.credentials = {"username": username, "password": password}

            return

        # The user has misconfigured their settings.py. Let them know.
        else:
            raise ValueError(f"AUTH_METHOD provided in the settings.py is invalid. Available AUTH_METHODS: {settings.AUTH_METHODS}\n")

    def prompt_not_none(self, message: str, secret: bool = False) -> str:
        """
        Prompts the user for input described in the message. If secret is set
        to true, user input is not shown. If the user doesn't put any input,
        warn them that they must input a value and call this function recursively.
        """
        # If secret set to False, allow user input to be visible and return it
        # If secret set to True, do not allow user input to be visible and return it
        prompt = input
        if secret:
            prompt = getpass

        value = prompt(message)

        if value == None:
            print("You cannot provide and empty value.\n")
            return self._prompt_not_one(message, secret)

        return value

    def prompt_yes_no_exit(self, message) -> None:
        """
        Prompts the user for yes or no input. The script will exit if anything
        except for a 'yes' answer is selected.
        """
        yn = input(message)

        # If user selects 'no' then exit the script, if the user selects 'yes'
        # then pass to continue the script, otherwise exit the script if the
        # user doesn't provide any valid selections.
        if yn == "n" or yn == "N":
            sys.exit(1)
        elif yn == "y" or yn == "Y":
            return
        else:
            print("Invalid option required. Must type 'y' for yes or 'n' for no.\n")
            sys.exit(1)
            