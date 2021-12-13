import random, re, string, sys, os

from importlib.util import find_spec
from importlib import import_module
from typing import List, Tuple, Dict

from core.BaseController import BaseController
from packages.tapipy.controllers.TapipyController import TapipyController
from utils.Logger import logger
from utils.cmd_to_class import cmd_to_class
from utils.str_to_cmd import str_to_cmd
from conf.settings import DEFAULT_PACKAGE, ACTION_FILTER_SUFFIX, PACKAGES_DIR
from packages.utils.aliases import aliases as utils_aliases
from utils.ConfigManager import configManager as config


class Router:
    """
    Commands and their options are passed into the router.
    The options are parsed and then the command is resolved.
    """
    tag_value_pattern: str
    kw_arg_tag_pattern: str
    cmd_option_pattern: str
    space_replacement: str

    def __init__(self):
        self.tag_value_pattern = r"([\w\r\t\n!@#$%^&*()\-+\{\}\[\]|\\\/:;\"\'<>?\|,.`~=]*)"
        self.kw_arg_tag_pattern = r"[-]{2}([\w]{1}[\w]*)"
        self.cmd_option_pattern = r"^[-]{1}[a-z]+[a-z_]*$"
        buffer = "[*]"
        self.space_replacement = buffer.join(random.choice(string.punctuation) for _ in range(5)) + buffer

    def _resolve_alias(self, name, aliases: Dict[str, List[str]]):
        for category, aliases in aliases.items():
            if name in aliases:
                return category

        return None

    def resolve(self, args: List[str]) -> Tuple[BaseController, List[str]]:
        try:
            # Controller name is the first argument
            if len(args) == 0:
                raise Exception("No category provided")
            category: str = args.pop(0)

            # Parse the rest of the arguments and extract the values
            (cmd, cmd_options, kw_args, args) = self._resolve_args(args)

            # Prevent users from bypassing the action filters and protected
            # methods by disallowing the cmd to contain the action filter
            # prefix, start with '_', or is one of the following:
            # [ "before", "after", "index" ]
            if (
                ACTION_FILTER_SUFFIX in cmd
                or cmd[0] == "_"
                or cmd in [ "before", "after" ]
            ):
                raise Exception(f"Category {category} has no command {cmd}")

        except Exception as e:
            logger.error(e)
            sys.exit()

        # Set the package
        current = config.get("current", "package")
        package = current if current is not None else DEFAULT_PACKAGE

        ################### STEPS TO CONTROLLER RESOLUTION ####################
        """
        - Check the 'utils' package for a controller with a method 
        that corresponds to the provded args. Dispatch if found.

        - If a utils controller is not found, check the 'tapipy' 
        package for a resource with an operation that corresponds to 
        the provided args
        
        - If 'tapipy' is not the current package, check the current package
        (found in the configs) for a controller with method that corresponds
        to the provided args
        """
        #######################################################################
        # Check for a utils controller that matches the args
        utils_ns = "packages.utils.controllers"

        # Check if the package has a controller by the provided name
        has_category = bool(find_spec(f"{utils_ns}.{cmd_to_class(category)}"))

        # Check if an alias for a category is being used. Will return 'None'
        # if no alias is found
        aliased_category = self._resolve_alias(category, utils_aliases)

        # If the package does not have a controller by the name provided but
        # does have an alias for that name, set that to the new category
        if has_category == False and bool(aliased_category):
            category = aliased_category

        # Import the controller and set the method(cmd) to be invoked
        if has_category or bool(aliased_category):
            module = import_module(f"{utils_ns}.{cmd_to_class(category)}", "./" )
            controller_class = getattr(module, f"{cmd_to_class(category)}")
            
            # Instantiate the controller class
            controller = controller_class()

            # Set the options and command
            controller.set_cmd(str_to_cmd(cmd))
            controller.set_cmd_options(cmd_options)
            controller.set_kw_args(kw_args)

            # Return the controller with command and options set
            return (controller, args)

        # If tapipy is the current package, invoke the operation on the resource.
        # NOTE Tapipy is a special package the breaks the pattern of other packages.
        # As a consequence, the 'category' and 'cmd' do not correlate to a controller 
        # and method respectively. The category is the 
        # resource(for which an alias may exist) and the cmd is the operation
        if package == "tapipy":
            controller = TapipyController()
            # TODO resolve aliases for tapipy package resource. Should be done
            # within the TapipyController itself
            controller.set_resource(category)
            
            # NOTE Some magic here.
            # Calling the index method on the tapipy controller determines the operation,
            # args, kwargs, and options itself
            if cmd == "index":
                (cmd, kw_args, args) = controller.index()

            controller.set_operation(cmd)
            controller.set_cmd_options(cmd_options)
            controller.set_kw_args(kw_args)

            return (controller, args)

        # No utils controller is found, nor is tapipy the current package.
        # Find a controller in the current package.
        package_ns = f"packages.{package}.controllers"

        # Check if the package has a controller by the provided name
        has_category = bool(find_spec(f"{package_ns}.{cmd_to_class(category)}"))

        # Import the aliases for this package if an aliases.py file exists in the
        # package
        package_aliases = {}
        if os.path.isfile(f"{PACKAGES_DIR}{package}/aliases.py"):
            alias_module = import_module(f"packages.{package}.aliases", "./")
            package_aliases = {}
            if hasattr(alias_module, "aliases"):
                package_aliases = getattr(alias_module, "aliases")

        # Check if an alias for a category is being used. Will return 'None'
        # if no alias is found
        aliased_category = self._resolve_alias(category, package_aliases)

        # If the package does not have a controller by the name provided but
        # does have an alias for that name, set that to the new category
        if has_category == False and bool(aliased_category):
            category = aliased_category

        if has_category or bool(aliased_category):
            # Import the current package controller
            module = import_module(f"packages.{package}.controllers.{cmd_to_class(category)}", "./" )
            controller_class: type[BaseController] = getattr(module, f"{cmd_to_class(category)}")
                
            # The controller class has a method by the command name.
            # Instantiate the controller class
            controller = controller_class()

            # Set the options and command
            controller.set_cmd(str_to_cmd(cmd))
            controller.set_cmd_options(cmd_options)
            controller.set_kw_args(kw_args)

            # Return the controller with command and options set.
            return (controller, args)

        # No controller was found in the current package by the name provided
        # in the args. Log the error and exit.
        logger.error(f"Category '{category}' not found in package '{package}'")
        sys.exit()

    def _parse_cmd_options(self, args: List[str]) -> Tuple[List[str], List[str]]:
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
                continue
            break

        # Remove the cmd_options from the args
        for index in sorted(option_indices, reverse=True):
            args.pop(index)

        return (cmd_options, args)

    def _parse_kw_args(self, args: List[str]) -> Tuple[Dict[str, str], List[str]]:
        """Keyword arguments are parsed specifically."""
        # Escape spaces in args
        escaped_args = self._escape_args(args)

        # Regex pattern for keyword args and their values
        regex = rf"(?<=[\s]){self.kw_arg_tag_pattern}[\s]+{self.tag_value_pattern}(?=[\s])*"
        pattern = re.compile(regex, re.MULTILINE | re.UNICODE)
        escaped_matches = dict(pattern.findall(" " + self._args_to_str(escaped_args)))
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

    def _resolve_args(self, args: List[str]) -> Tuple[
            str,
            str,
            Dict[str, str],
            List[str]
        ]:
        """Options are parsed form the args to resolve the args."""
        # Parse the options from the args.
        (cmd_options, args) = self._parse_cmd_options(args)

        # Get the command for the controller from the modified args list.
        if len(args) < 1:
            args.append("index")

        cmd = args.pop(0)

        # Parse the keyword arguments and their values from the args list
        (kw_args, args) = self._parse_kw_args(args)

        return (
            cmd,
            cmd_options,
            kw_args,
            args
        )

    def _args_to_str(self, args) -> string:
        """Converts arguments to 'string' type for easier parsing."""
        arg_str = ""
        for arg in args:
            arg_str = arg_str + " " + str(arg)

        return arg_str.lstrip(" ")

    def _escape_args(self, args: List[str]) -> list:
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
