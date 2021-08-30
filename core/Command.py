from tapipy.tapis import Tapis
import sys

class Command:
    options_set = { "--default": [] }
    options = []
    action = "help"

    def __init__(self):
        # @TODO import option set if one exists
        pass

    def help(self, *args):
        print(f"Help command for {type(self).__name__} has not yet been supported")

    def set_action(self, action: str) -> None:
        if action not in dir(self):
            raise ValueError(f"Command {type(self).__name__} has no action '{action}'")

        self.action = action

    def set_option_set(self, option_set: dict = {}):
        self.option_set = option_set
    
    def set_options(self, options: list):
        self.options = options

    def execute(self, client: Tapis, args) -> None:
        method = getattr(self, self.action)
        method(client, *args)
