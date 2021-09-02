from importlib import import_module
from core.Logger import Logger
import re, sys

class Resolver:
    action_index = 1
    logger = None

    def __init__(self):
        self.logger = Logger()

    def resolve(self, args: list) -> None:
        # Import the command module and instantiate the class
        module = None
        try:
            module = import_module( f"commands.{args[0].capitalize()}", "./" )
        except ModuleNotFoundError:
            self.logger.error(f"Invalid Command. '{args[0]}' command not implemented")
            sys.exit(1)

        self.set_command(getattr(module, f"{args[0].capitalize()}")())

        # Set the options on the command.
        options = self.parse_options(args[1:])
        self.command.set_options(options)

        # Set the action on the command.
        self.command.set_action(args[self.action_index])

        # Return the command with action and options set.
        # Every element in the args list after the action index are arguments
        # for the command.
        return (self.command, args[self.action_index+1:])

    def parse_options(self, args):
        # Regex pattern for options.
        option_pattern = re.compile(r"^[-]{1,2}[a-z]+[a-z_]*$")

        # First arg in the args list is the command.
        # For every option found in the args list, increment the action_index
        # by 1. If none are found, then the action name is at index 1.
        options = []
        for option in args:
            if re.match(option_pattern, option):
                options.append(option)
                self.action_index += 1
                continue
            break

        return options
            
    def set_command(self, command):
        self.command = command