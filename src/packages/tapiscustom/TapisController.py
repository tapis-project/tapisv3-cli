import inspect

from tapipy.tapis import Tapis

from core.BaseController import BaseController
from packages.tapis.Authenticator import Authenticator as Auth


class TapisController(BaseController):
    client: Tapis

    def __init__(self):
        BaseController.__init__(self)

    def before(self):
        try:
            self.client = Auth().authenticate()
            if self.client is None:
                self.exit(1)
        except SystemExit:
            self.exit(1)
        except:
            raise ValueError(f"Unable to authenticate user")
        
