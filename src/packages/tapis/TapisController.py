import re

from tapipy.tapis import Tapis

from conf import settings
from core.BaseController import BaseController
from packages.tapis.Authenticator import Authenticator as Auth


class TapisController(BaseController):
    """Base Tapis Controller."""
    client: type[Tapis]

    def __init__(self):
        BaseController.__init__(self)

    def before(self):
        try:
            self.client = Auth().authenticate()
            if self.client is None:
                self.exit()
        except SystemExit:
            self.exit()
        except:
            raise ValueError(f"Unable to authenticate user using AUTH_METHOD {settings.AUTH_METHOD}\n")

    def methods(self) -> None:
        """Returns all of the methods associated with a particular controller."""
        all_methods = dir(getattr(self.client, type(self).__name__.lower()))
        methods = []

        pattern = re.compile(r"^[_]{1:2}[\w]+")
        for method in all_methods:
            if not re.match(pattern, method):
                methods.append(method)

        self.logger.log(methods)
        return
