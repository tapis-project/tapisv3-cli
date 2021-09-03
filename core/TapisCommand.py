from tapipy.tapis import Tapis
from core.Command import Command
from core.Authenticator import Authenticator as Auth
from types import Union
from configs import settings
import re

class TapisCommand(Command):

    client: Union[Tapis, None] = None

    def __init__(self):
        Command.__init__(self)
        try:
            self.client = Auth().authenticate()
        except:
            raise ValueError("Unable to authenticate user using AUTH_METHOD {settings.AUTH_METHOD}")

    def help(self):
        all_methods = dir(getattr(self.client, type(self).__name__.lower()))
        methods = []

        pattern = re.compile(r"^[_]{2}[\w]+")
        for method in all_methods:
            if not re.match(pattern, method):
                methods.append(method)

        self.logger.log(methods)

    def checkhealth(self):
        command_name = type(self).__name__
        command = getattr(self.client, command_name.lower())
        if hasattr(command, "checkHealth"):
            self.logger.log(command.checkHealth())
            return

        self.logger.error(f"Command {type(self).__name__} has no action 'checkHealth'")
        self.exit(1)

    def healthcheck(self):
        command_name = type(self).__name__
        command = getattr(self.client, command_name.lower())
        if hasattr(command, "healthCheck"):
            self.logger.log(command.healthCheck())
            return

        self.logger.error(f"Command {type(self).__name__} has no action 'healthCheck'")
        self.exit(1)

    def readycheck(self):
        command_name = type(self).__name__
        command = getattr(self.client, command_name.lower())
        if hasattr(command, "readyCheck"):
            self.logger.log(command.readyCheck())
            return

        self.logger.error(f"Command {type(self).__name__} has no action 'readyCheck'")
        self.exit(1)

    def ready(self):
        command_name = type(self).__name__
        command = getattr(self.client, command_name.lower())
        if hasattr(command, "ready"):
            self.logger.log(command.ready())
            return

        self.logger.error(f"Command {type(self).__name__} has no action 'ready'")
        self.exit(1)
