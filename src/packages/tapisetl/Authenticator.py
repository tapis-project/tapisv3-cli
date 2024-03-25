import sys

from tapipy.tapis import Tapis
from tapipy.errors import AuthenticationError

from conf import settings
from packages.tapis.settings import BASE_URL
from utils.ConfigManager import config_manager
from utils.Logger import Logger


class Authenticator:
    def __init__(self, base_url=BASE_URL):
        self.base_url: str = base_url
        self.auth_methods = settings.AUTH_METHODS
        self.logger = Logger()

    def authenticate(self):

        current_user = config_manager.get_current_user()

        if current_user == None:
            self.logger.warn(f"No current active user. Run the following: `tapis login`")
            return

        profile = config_manager.get_profile(current_user)

        try:
            client = Tapis(
                base_url=profile["base_url"],
                username=current_user,
                jwt=profile["jwt"]
            )
            
            return client
        except Exception:
            self.logger.warn("Authentication Error: Run the following: `tapis login`")
            sys.exit(1)
