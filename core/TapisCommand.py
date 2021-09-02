from core.Command import Command
import re

class TapisCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def help(self, client):
        all_methods = dir(getattr(client, type(self).__name__.lower()))
        methods = []

        pattern = re.compile(r"^[_]{2}[\w]+")
        for method in all_methods:
            if not re.match(pattern, method):
                methods.append(method)

        self.logger.log(methods)

    def checkhealth(self, client):
        command_name = type(self).__name__
        command = getattr(client, command_name.lower())
        if hasattr(command, "checkHealth"):
            self.logger.log(command.checkHealth())
            return

        self.logger.error(f"Command {type(self).__name__} has no action 'checkHealth'")
        self.exit(1)

    def healthcheck(self, client):
        command_name = type(self).__name__
        command = getattr(client, command_name.lower())
        if hasattr(command, "healthCheck"):
            self.logger.log(command.healthCheck())
            return

        self.logger.error(f"Command {type(self).__name__} has no action 'healthCheck'")
        self.exit(1)

    def readycheck(self, client):
        command_name = type(self).__name__
        command = getattr(client, command_name.lower())
        if hasattr(command, "readyCheck"):
            self.logger.log(command.readyCheck())
            return

        self.logger.error(f"Command {type(self).__name__} has no action 'readyCheck'")
        self.exit(1)

    def ready(self, client):
        command_name = type(self).__name__
        command = getattr(client, command_name.lower())
        if hasattr(command, "ready"):
            self.logger.log(command.ready())
            return

        self.logger.error(f"Command {type(self).__name__} has no action 'ready'")
        self.exit(1)
