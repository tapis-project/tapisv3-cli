import os, sys
from configs import settings
from configparser import ConfigParser
from getpass import getpass

class Configuration:
    """
    Writes user credentials to the credentials file based on the AUTH_METHOD 
    provided in the settings.py
    """
    auth_method: str = settings.AUTH_METHOD
    config: ConfigParser = None
    credentials: dict = {}

    def __init__(self):
        # If the credentials file specified in the settings does not exist,
        # create it.
        if not os.path.isfile("../" + settings.CREDENTIALS_FILE):
            print(f"Creating config file '{settings.CREDENTIALS_FILE}'")
            file = open("../" + settings.CREDENTIALS_FILE, "w")
            file.write("[credentials]")
            file.close()

        # Intialize and set the configparser to the Configuration object and
        # get the credentials from the config file
        self.config = ConfigParser()
        self.config.read(settings.CREDENTIALS_FILE)

        # Initialize the ConfigParser and add the credntials from the config 
        # file to this  Configuration object's credentials dict
        for key in self.config["credentials"]:
            self.credentials[key] = self.config["credentials"][key]


    def configure(self):
        """
        Checks if the users credentials exist for the current authentication method 
        set in the settings.py file. If it doesn't, the user will be prompted to 
        provide the correct credentials for the defined authentication method.
        """

        if settings.AUTH_METHOD not in settings.AUTH_METHODS:
            raise ValueError(f"Misconfigured settings.py. The AUTH_METHOD provided does not exist in the list AUTH_METHODS. AUTH_METHOD={settings.AUTH_METHODS}")

        # Check the current authentication method and prompt the user to provide
        # the appropriate credentials if they do not exist.
        if settings.AUTH_METHOD == settings.PASSWORD:

            # Fetch the username and password from the credentials file if
            # they exist.
            username = self.config["credentials"]["username"]
            password = self.config["credentials"]["password"]

            # If username and password exist, return nothing.
            if username and password:
                return

            # Prompt user for username and password
            print("\nTACC credentials not found.\nProvide TACC username and password.\n")
            
            self.prompt_yes_no_exit("Continue? [y/n]: ")

            # Prompt the username to create a username and password
            self.config["credentials"]["username"] = self.prompt_not_none("Username: ")
            self.config["credentials"]["password"] = self.prompt_not_none("Password 🔒: ", secret=True)
            
            # Save the credentials 
            with open(settings.CREDENTIALS_FILE, "w") as file:
                self.config.write(file)

            # Set the username and password in the Configuration's credientials
            # dict
            self.credentials = {username: username, password: password}

            return

        # The user has misconfigured their settings.py. Let them know.
        else:
            raise ValueError(f"AUTH_METHOD provided in the settings.py is invalid. Available AUTH_METHODS: {settings.AUTH_METHODS}")

    def prompt_not_none(self, message: str, secret: bool = False) -> str:
        """
        Prompts the user for input described in the message. If secret is set
        to true, user input is not shown. If the user doesn't put any input,
        warn them that they must input a value and call this function recursively
        """
        # If secret set to False, allow user input to be visible and return it
        if not secret:
            value = input(message)

        # If secret set to True, do not allow user input to be visible and return it
        value = getpass(message)

        if value == None:
            print("You cannot provide and empty value.")
            return self._prompt_not_one(message, secret)

        return value

    def prompt_yes_no_exit(self, message):
        yn = input(message)

        # If use select no, exit the script
        if yn == "n" or yn == "N":
            sys.exit()

        # If user selects yes, pass to continue the script
        elif yn == "y" or yn == "Y":
            return

        # If user doesn't provide any valid selections, exit the script
        else:
            print("Invalid option required. Must type 'y' for yes or 'n' for no.")
            exit(1)
            