"""
Handles the command setting, command execution, and command help 
functionality for the TAPIS CLI (adaptable to use non-TAPIS commands
if the user creates new ones and a parser for non-TAPIS categories).
"""

import re
import sys
import types

from typing import List, Dict, Any

from utils.module_loader import class_loader as load
from utils.Logger import Logger
from core.OptionSet import OptionSet
from core.AbstractView import AbstractView
from options.options_sets import option_registrar

class Controller:
    """ 
    Each category has the same methods available to get/set/execute.
    If the user wants to add non-TAPIS categories and commands, the new parser
    should inherit from this category. See 'TapipyCategory.py' for an example.
    """
    option_set: type[OptionSet]
    cmd_options: list
    kw_args: Dict[str, str]
    arg_options: Dict[str, Dict[str, str]]
    command: str
    override_exec: bool
    logger: type[Logger]
    exit: callable
    arg_option_tag_pattern: str
    view: type[AbstractView]

    def __init__(self):
        self.option_set = option_registrar.get_option_set(type(self).__name__)
        self.cmd_options = []
        self.kw_args = {}
        self.arg_options = {}
        self.command = "help"
        self.override_exec = False
        self.logger = Logger()
        self.exit = sys.exit
        self.arg_option_tag_pattern = r"([-]{1}[\w]{1}[\w]*)"
        self.view = None

    def help(self):
        """
        \nGeneral usage:
        $tapis [category] [options] [command] [args/keyword args]
        \nExamples:
        - tapis systems get [systemId]
        - tapis systems getSystem --systemId [systemId]
        - tapis files upload [systems] [path/to/local/file] [destination/folder]
        - tapis systems update [path/to/definition/file]
        - tapis apps create [path/to/definition/file]
        - tapis jobs submit [appName] [appVersion]
        \nCommands:"""
        
        print(self.help.__doc__)
        methods = self.get_methods(self)
        for method in methods:
            print(f"\t- {method}")

    def set_command(self, command: str) -> None:
        """
        Sets the command to be executed in a specific category. 
        EX: apps = category, list = command
        """
        if command not in dir(self):
            self.logger.error(f"Category {type(self).__name__} has no command '{command}'\n")
            self.exit(1)
        self.command = command

        return
    
    def set_cmd_options(self, cmd_options: list) -> None:
        self.cmd_options = cmd_options

        return

    def set_kw_args(self, kw_args: Dict[str, str]) -> None:
        self.kw_args = kw_args
        return

    def invoke(self, args: List[str]) -> None:
        if self.override_exec:
            return

        method = getattr(self, self.command)
        method(*args)

        return

    def get_methods(self, instance: object) -> list:
        """Returns all of the methods that are available for the specified category."""
        # Get all props of of the instance.
        class_props = dir(instance)

        # Remove the dunders.
        props = []
        pattern = re.compile(r"^[_]{1:2}[\w]+")
        for prop in class_props:
            if not re.match(pattern, prop):
                props.append(prop)

        # Remove all class properties that are not functions.
        methods = []
        for prop_name in props:
            prop = getattr(instance, prop_name)
            if isinstance(prop, types.MethodType):
                methods.append(prop_name)

        return methods

    def parse_args(self, args: list[str]):
        pos_args = []
        arg_opt_indices = []
        option_names = self.option_set.get_names()

        for index, arg in enumerate(args):
            # This line will skip the indices of arg option parameters 
            # that were added in previous iterations
            if index in arg_opt_indices:
                continue

            # If the arg doesn't match the arg_option_tag_pattern, then it
            # is a positional argument
            if re.match(rf"{self.arg_option_tag_pattern}", arg) == None:
                pos_args.append(arg)
                continue

            # Validate user provided options against the category's option set
            if arg not in option_names:
                raise Exception(f"{arg} is not a valid option for command {self.command}")

            # Gets the option by name from the OptionSet
            option = self.option_set.get_by_name(arg)

            # Make a list of the params and calculate the len
            params = list(option.params.keys()) if option.params is not {} else []
            params_len = len(params)

            # Create a list of the remaining args. This will be used to check if
            # there are a sufficient number args left to satisfy the current option's
            # parameter requirements
            remaining_args = args[index+1:]

            # If there are fewer remaining args than params, raise an exception
            if len(remaining_args) < params_len:
                raise Exception(f"Option {arg} expects {params_len} params: {params}. Only {len(remaining_args)} params providied")
            
            # Calculate the indices of the args that correspond to the current
            # option's params
            next_arg_index = index + 1
            last_arg_index = next_arg_index + params_len
            arg_option_vals = args[next_arg_index:last_arg_index]
            
            # Add the to the arg_opt_indices list so that we can skip it
            # in subsequent iterations
            for index in range(next_arg_index, last_arg_index):
                arg_opt_indices.append(index)

            # Create a nested dictionary with arg_options as the key, and a
            # value of { param_name: option_value }
            self.arg_options[arg] = {}
            for index, val in enumerate(arg_option_vals):
                self.arg_options[arg][params[index]] = val

            continue
        
        return pos_args

    def set_view(self, name: str, data: Any) -> None:
        view_class = load(f"views.{name}", name)
        if view_class is None:
            raise Exception("View '{name}' does not exist")

        self.view = view_class(data)

        return

            
            
