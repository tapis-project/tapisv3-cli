from tapipy.tapis import Tapis
from core.Logger import Logger
import sys, inspect

class Command:
    options_set = { "--default": [] }
    options = []
    action = "help"
    logger = None
    exit = sys.exit

    def __init__(self):
        self.logger = Logger()

    def help(self, *args):
        self.logger.warn(f"Help command for {type(self).__name__} has not yet been supported")

    # Run the list method on child class, then use return value
    # to run get action
    # TODO Implement bash dialog
    def select(self, *args):
        self.logger.warn(f"Select command for {type(self).__name__} has not yet been supported")

    def set_action(self, action: str) -> None:
        if action not in dir(self):
            self.logger.error(f"Command {type(self).__name__} has no action '{action}'")
            self.exit(1)
        self.action = action

    def set_option_set(self, option_set: dict = {}):
        self.option_set = option_set
    
    def set_options(self, options: list):
        self.options = options

    def execute(self, client: Tapis, args) -> None:
        method = getattr(self, self.action)
        method(client, *args)
