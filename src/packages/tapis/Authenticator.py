import sys

from tapipy.tapis import Tapis

from conf import settings
from packages.tapis.settings import BASE_URL
from utils.ConfigManager import configManager as config
from utils.Logger import Logger


class Authenticator:
    base_url: str
    auth_methods: str

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.auth_methods = settings.AUTH_METHODS
        self.logger = Logger()

    def authenticate(self) -> Tapis:
        username = config.get("current", "profile")

        if bool(username) == False:
            self.logger.warn("CLI has not been configured. Run the following `tapis configure`")
            return

        profile = config.get_section(f"profile.{username}")

        # Authenticate using the provided auth method. Raise exception
        # if provided credentials do not meet requirements.
        # TODO self.validate_credentials(profile.auth_method, config.credentials)
        if profile["auth_method"] == settings.PASSWORD:
            try:
                client = Tapis(
                    base_url=self.base_url,
                    username=username,
                    password=profile[settings.PASSWORD.lower()]
                )
                client.get_tokens()
                return client
            except Exception as e:
                # TODO Make better
                error = e
                if hasattr(e, "message"):
                    error = e.message
                self.logger.error(error)
                sys.exit(1)

        else:
            raise ValueError(f"Invalid auth_method: {profile.auth_method}. Valid auth_method: {settings.AUTH_METHODS}")

    def validate_credentials(self, auth_method: str, credentials: dict) -> None:
        # TODO validate creds based on the current profile's auth method.
        # throw error if creds don't validate

        return

    def keys_in_dict(self, keys: list, creds_dict: dict) -> bool:
        for key in keys:
            if key not in creds_dict:
                return False

        return True
