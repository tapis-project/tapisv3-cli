import re
import sys
import types
import inspect
from typing import List, Dict, Any

from core.AbstractView import AbstractView
from core.OptionSet import OptionSet
from packages.shared.options.options_sets import option_registrar
from utils.Logger import Logger
from utils.module_loader import class_loader as load
from conf.settings import ACTION_FILTER_SUFFIX
from helpers.help_formatter import help_formatter as formatter


class BaseController:
    """
    Base class for categories.
    """
    option_set: type[OptionSet]
    cmd_options: list
    kw_args: Dict[str, str]
    arg_options: Dict[str, Dict[str, str]]
    cmd: str
    override_exec: bool
    logger: type[Logger]
    exit: callable
    arg_option_tag_pattern: str
    view: type[AbstractView]
    is_action: bool

    def __init__(self):
        self.option_set = option_registrar.get_option_set(type(self).__name__)
        self.cmd_options = []
        self.kw_args = {}
        self.arg_options = {}
        self.cmd = "help"
        self.override_exec = False
        self.logger = Logger()
        self.arg_option_tag_pattern = r"([-]{1}[\w]{1}[\w]*)"
        self.view = None
        self.is_action = False

    def before(self):
        pass

    def after(self):
        pass

    def index(self):
        self.logger.log(f"\n{self.__doc__}")
        self.help()

    def help(self):
        formatter.add_usage(f"$tapis [category] [options] [command] [args/keyword args]")
        methods = [ method for method in dir(self) if (
            (not method.startswith(("_", "__")))
            and callable(getattr(self, method))
            and method not in dir(BaseController)
        )]
        
        for method in methods:
            pos_args = inspect.getfullargspec(getattr(self, method)).args
            if "self" in pos_args:
                pos_args.remove("self")
            formatter.add_command(
                method.replace("_Action", ""), 
                positional_args=pos_args
            )
            
        formatter.add_options(self.option_set.options)

        self.logger.log(formatter.build())

    def set_cmd(self, cmd: str) -> None:
        """
        Sets the command to be executed in a specific category.
        EX: apps = category, list = command
        """
        cmd_action = cmd + ACTION_FILTER_SUFFIX
        if cmd not in dir(self):
            if cmd_action not in dir(self):
                self.logger.error(f"Category {type(self).__name__} has no command '{cmd}'\n")
                self.exit(1)
            self.is_action = True

        self.cmd = cmd_action if self.is_action else cmd

        return

    def set_cmd_options(self, cmd_options: list) -> None:
        """Sets the options for a command."""
        self.cmd_options = cmd_options

        return

    def set_kw_args(self, kw_args: Dict[str, str]) -> None:
        """Sets the keyword arguments for a command."""
        self.kw_args = kw_args

        return

    def invoke(self, args: List[str]) -> None:
        """Passes input args to the command."""
        # TODO Check that self.cmd is a method
        # TODO Prevent users from calling parent class methods
        if self.override_exec:
            return

        # Run the 'before' action filter
        if self.is_action:
            self.before()

        method = getattr(self, self.cmd)
        method(*args)

        # Run the 'after' action filter
        if self.is_action:
            self.after()

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
        """Parses the arguments found in the input CLI command."""
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
                raise Exception(f"{arg} is not a valid option for command {self.cmd}")

            # Gets the option by name from the OptionSet
            option = self.option_set.get_by_name(arg)

            # Make a list of the params and calculate the length of the list
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
        """Loads a view if it exists"""
        view_class = load(f"packages.shared.views.{name}", name)
        if view_class is None:
            raise Exception(f"View '{name}' does not exist")

        self.view = view_class(data)
        return

    def exit():
        sys.exit()
