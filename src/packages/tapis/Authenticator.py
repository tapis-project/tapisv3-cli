import sys, time

from conf import settings
from utils.ConfigManager import config_manager
from utils.Logger import Logger


class Authenticator:
    def __init__(self):
        self.logger = Logger()

    def authenticate(self):
        # TODO NOTE FIXME BUG Import taking a long time. move to top when resolved
        from tapipy.tapis import Tapis
        from tapipy.errors import UnauthorizedError

        current_user = config_manager.get_current_user()

        if current_user == None:
            self.logger.warn(f"No current active user. Run the following `tapis login`")
            return

        login = config_manager.get_current_login(current_user)

        try:
            client = Tapis(
                base_url=login["base_url"],
                username=login["username"],
                jwt=login["jwt"]
            )
            
            return client
        except Exception:
            self.logger.warn("Authentication Error: Run the following: `tapis login`")
            sys.exit(1)
