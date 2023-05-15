import sys, time

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
        # TODO NOTE FIXME Import taking a long time. move to top when resolved
        from tapipy.tapis import Tapis
        current_user = config_manager.get_current_user()

        if current_user == None:
            self.logger.warn(f"No current active user. Run the following `tapis login`")
            return

        profile = config_manager.get_profile(current_user)

        try:
            client = Tapis(
                base_url=profile["base_url"],
                username=current_user,
                jwt=profile["jwt"]
            )
            
            return client
        except Exception as e:
            self.logger.error(f"Authentication Error: {e}")
            sys.exit(1)
