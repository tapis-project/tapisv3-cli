import sys
from typing import Union

from tapipy.tapis import Tapis

from conf import settings
from packages.tapis.settings import BASE_URL
from utils.ConfigManager import ConfigManager
from utils.Logger import Logger


class Authenticator:
    """Authorization credentials are parsed here."""
    base_url: str
    auth_methods: str

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.auth_methods = settings.AUTH_METHODS
        self.logger = Logger()
        self.conf = ConfigManager()

    def authenticate(self, auth_method: str = settings.DEFAULT_AUTH_METHOD) -> Union[Tapis, None]:
        """
        The user is authenticated by the TAPIS client.
        Only password authentication is implemented for now.
        """
        # If there are no credentials in the credentials dict, throw error
        if not bool(self.conf.credentials):
            # Add the credentials from the config file to
            # this Configuration object's credentials dict.
            self.logger.error("Tapis CLI not configured.")
            self.logger.log("Run the following commands in order:\n`tapis cli configure`\n`tapis auth configure`")
            sys.exit(1)

        # Authenticate using the provided auth method. Raise exception
        # if provided credentials do not meet requirements.
        if auth_method == settings.PASSWORD:
            self.validate_credentials(auth_method, self.conf.credentials)
            try:
                client = Tapis(
                    base_url=self.base_url,
                    username=self.conf.credentials["username"],
                    password=self.conf.credentials["password"]
                )
                client.get_tokens()
                return client
            except:
                e = sys.exc_info()[0]
                self.logger.log(e.message)
        else:
            raise ValueError(f"Invalid auth_method: {auth_method}. Valid auth_method: {settings.AUTH_METHODS}\n")

    def validate_credentials(self, auth_method: str, credentials: dict) -> None:
        """Checks to see if the user's credentials exist already."""
        if auth_method == "PASSWORD":
            if not self.keys_in_dict(["username", "password"], credentials):
                raise ValueError("Provided credentials must contain a 'username' and 'password'\n")

        return

    def keys_in_dict(self, keys: list, creds_dict: dict) -> bool:
        """Iterates through the dictionary of known keys to find user credentials."""
        for key in keys:
            if key not in creds_dict:
                return False

        return True