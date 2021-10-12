import random
import re
import string

from importlib.util import find_spec
from importlib import import_module
from typing import List, Tuple, Dict

from core.Controller import Controller
from core.TapipyController import TapipyController
from utils.ConfigManager import ConfigManager
from utils.Logger import Logger
from conf.settings import DEFAULT_PACKAGE


class Router:
    """
    Commands and their options are passed into the router.
    The options are parsed and then the command is resolved.
    """
    command_index: int
    logger: type[Logger]
    conf: ConfigManager
    tag_value_pattern: str
    kw_arg_tag_pattern: str
    cmd_option_pattern: str
    space_replacement: str

    def __init__(self):
        self.command_index = 0
        self.logger = Logger()
        self.conf = ConfigManager()
        self.tag_value_pattern = r"([\w\r\t\n!@#$%^&*()\-+\{\}\[\]|\\\/:;\"\'<>?\|,.`~=]*)"
        self.kw_arg_tag_pattern = r"[-]{2}([\w]{1}[\w]*)"
        self.cmd_option_pattern = r"^[-]{1}[a-z]+[a-z_]*$"
        buffer = "[*]"
        self.space_replacement = buffer.join(random.choice(string.punctuation) for _ in range(5)) + buffer

    def resolve(self, args: List[str]) -> Tuple[Controller, List[str]]:
        """The command is resolved here."""
        # Controller name is the first argument
        controller_name: str = args.pop(0)

        # Parse the rest of the arguments and extract the values
        (cmd_name, cmd_options, kw_args, args) = self.resolve_args(args)

        # Fetch the default package from the configs
        package = DEFAULT_PACKAGE
        if (
            self.conf.has_key("current", "package")
            and bool(self.conf.get("current", "package"))
        ):
            package = self.conf.get("current", "package")

        ################### STEPS TO CONTROLLER RESOLUTION ####################
        """
        - Check the 'core' package for a controller with a method 
        that corresponds to the provded args. Dispatch if found.

        - If a core controller is not found, check the 'current' 
        package(found in the configs) for a controller with a method 
        that corresponds to the provided args
        
        - If a current package controller or method is not found, dispatch 
        the current OpenApiController (TapipyController)
        """
        #######################################################################
        core_controller_ns = "packages.core.controllers"
        if find_spec(f"{core_controller_ns}.{controller_name.capitalize()}") is not None:
            module = import_module(f"{core_controller_ns}.{controller_name.capitalize()}", "./" )
            controller_class: type[Controller] = getattr(module, f"{controller_name.capitalize()}")

            if hasattr(controller_class, cmd_name):
                # The controller class has a method by the command name.
                # Instantiate the controller class
                controller = controller_class()

                # Set the options and command
                controller.set_command(cmd_name)
                controller.set_cmd_options(cmd_options)
                controller.set_kw_args(kw_args)

                # Return the controller with command and options set.
                return (controller, args)

        package_controller_ns = f"packages.{package}.controllers"
        if find_spec(f"{package_controller_ns}.{controller_name.capitalize()}") is not None:
            # Import the current package controller
            module = import_module(f"packages.{package}.controllers.{controller_name.capitalize()}", "./" )
            controller_class: type[Controller] = getattr(module, f"{controller_name.capitalize()}")

            if not hasattr(controller_class, cmd_name):
                # If the command being invoked doesn't exist on the controller,
                # instantiate an TapipyController
                controller = TapipyController()
                # Set the resource, operation, and options
                controller.set_resource(controller_name)
                controller.set_operation(cmd_name)
                controller.set_cmd_options(cmd_options)
                controller.set_kw_args(kw_args)

                return (controller, args)

            # The controller class has a method by the command name.
            # Instantiate the controller class
            controller = controller_class()

            # Set the options and command
            controller.set_command(cmd_name)
            controller.set_cmd_options(cmd_options)
            controller.set_kw_args(kw_args)

            # Return the controller with command and options set.
            return (controller, args)

        # If a user-defined controller doesn't exist, return an instance
        # of core.TapipyController
        controller = TapipyController()

        # Set the resource, operation, and options
        controller.set_resource(controller_name)
        controller.set_operation(cmd_name)
        controller.set_cmd_options(cmd_options)
        controller.set_kw_args(kw_args)

        return (controller, args)

    def parse_cmd_options(self, args: List[str]) -> Tuple[List[str], List[str]]:
        """Parse the options that precede the command"""
        # Regex pattern for options.
        pattern = re.compile(rf"{self.cmd_option_pattern}")
        # Iterate through the args until no more options are found
        cmd_options = []
        option_indices = []
        for index, option in enumerate(args):
            if pattern.match(option):
                cmd_options.append(option)
                option_indices.append(index)
                self.command_index += 1
                continue
            break

        # Remove the cmd_options from the args
        for index in sorted(option_indices, reverse=True):
            args.pop(index)

        return (cmd_options, args)

    def parse_kw_args(self, args: List[str]) -> Tuple[Dict[str, str], List[str]]:
        """Keyword arguments are parsed specifically."""
        # Escape spaces in args
        escaped_args = self.escape_args(args)

        # Regex pattern for keyword args and their values
        regex = rf"(?<=[\s]){self.kw_arg_tag_pattern}[\s]+{self.tag_value_pattern}(?=[\s])*"
        pattern = re.compile(regex, re.MULTILINE | re.UNICODE)
        escaped_matches = dict(pattern.findall(" " + self.args_to_str(escaped_args)))
        unescaped_matches = self.unescape_matches(escaped_matches)

        # Convert the dictionary of escaped matches into a list
        key_vals = []
        for items in unescaped_matches.items():
            # Append '--' to the value of every item in the key_vals list
            # with an even index. The double dash was removed while parsing
            # and it needs to be added back in order to remove it from the args list
            for index, item in enumerate(items):
                item = f"--{item}" if index % 2 == 0 else item
                key_vals.append(item)

        # Remove the keywords args and their values from args
        modified_args = []
        for arg in args:
            if arg not in key_vals:
                modified_args.append(arg)

        return (unescaped_matches, modified_args)

    def resolve_args(self, args: List[str]) -> Tuple[
            str,
            str,
            Dict[str, str],
            List[str]
        ]:
        """Options are parsed form the args to resolve the args."""
        # Parse the options from the args. This also determines the
        # index of the command name via self.command_index
        (cmd_options, args) = self.parse_cmd_options(args)

        # Get the command for the controller from the modified args list.
        cmd_name = args.pop(0)

        # Parse the keyword arguments and their values from the args list
        (kw_args, args) = self.parse_kw_args(args)

        return (
            cmd_name,
            cmd_options,
            kw_args,
            args
        )

    def args_to_str(self, args) -> string:
        """Converts arguments to 'string' type for easier parsing."""
        arg_str = ""
        for arg in args:
            arg_str = arg_str + " " + str(arg)

        return arg_str.lstrip(" ")

    def escape_args(self, args: List[str]) -> list:
        """
        A list of args is taken and all spaces are replaced with the
        space replacement defined in the class initialization.
        """
        escaped_args = []
        for arg in args:
            escaped_args.append(arg.replace(" ", self.space_replacement))

        return escaped_args

    def unescape_matches(self, matches: Dict[str, str]) -> dict:
        """Replaces 'space replacements' (defined in the class initialization) with spaces."""
        unescaped_matches = {}
        for key, value in matches.items():
            key = key.replace(self.space_replacement, " ")
            value = value.replace(self.space_replacement, " ")
            unescaped_matches[key] = value

        return unescaped_matches
