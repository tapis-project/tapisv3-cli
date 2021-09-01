from core.Command import Command
import re

class TapisCommand(Command):
    def __init__(self):
        Command.__init__(self)

    # TODO Remove
    def dirs(self, client):
        all_methods = dir(getattr(client, type(self).__name__.lower()))
        methods = []

        pattern = re.compile(r"^[_]{2}[\w]+")
        for method in all_methods:
            if not re.match(pattern, method):
                methods.append(method)

        self.logger.log(methods)