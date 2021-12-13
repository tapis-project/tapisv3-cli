import re
import sys
import os
import inspect
from typing import List, Dict, Any

from core.AbstractView import AbstractView
from core.OptionSet import OptionSet
from core.SettingSet import SettingSet
from packages.shared.options.options_sets import option_registrar
from utils.Logger import Logger
from utils.module_loader import class_loader as load
from conf.settings import ACTION_FILTER_SUFFIX
from helpers.help_formatter import help_formatter as formatter
from utils.Prompt import prompt
from utils.ConfigManager import configManager as config
from conf.settings import PACKAGES_DIR
from importlib import import_module


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
        self.settings_pattern = r"([A-Z]+[A-Z_]*)"
        self.view = None
        self.is_action = False
        self.config = config
        self.settings = self.init_settings()

    def before(self):
        pass

    def after(self):
        pass

    def index(self):
        self._select_Action()

    def help(self):
        formatter.add_usage(f"$tapis [category] [options] [command] [args/keyword args]")
        
        for method in self.get_methods():
            pos_args = inspect.getfullargspec(getattr(self, method)).args
            if "self" in pos_args:
                pos_args.remove("self")
            formatter.add_command(
                method.replace("_Action", ""), 
                positional_args=pos_args
            )
            
        formatter.add_options(self.option_set.options)

        self.logger.log(formatter.build())

    def get_methods(self):
        return [ method for method in dir(self) if (
            (not method.startswith(("_", "__")))
            and callable(getattr(self, method))
            and method not in dir(BaseController)
        )]

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

    def invoke(self, args: List[str], kwargs: Dict[str, str] = {}) -> None:
        """Passes input args to the command."""
        # TODO Check that self.cmd is a method
        # TODO Prevent users from calling parent class methods
        if self.override_exec:
            return

        # Run the 'before' action filter
        if self.is_action:
            self.before()

        method = getattr(self, self.cmd)
        method(*args, **kwargs)

        # Run the 'after' action filter
        if self.is_action:
            self.after()

        return

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

    # TODO add tab autocomplete for files and dirs
    def _select_Action(self) -> None:
        # Get the methods for this controller and remove the select_Action
        methods = self.get_methods()

        # Generate a dictionary where the key is the name of the method
        # without the suffix "_Action" and the value is the method attr itself
        op_map = {}
        for op_name in methods:
            op_map[op_name.replace("_Action", "")] = getattr(self, op_name)

        # Prompt the user to select an operation to perform over the system with
        # the selection system_id
        action = prompt.select("Perform action", [ op for op, _ in op_map.items() ])

        # Set the cmd to be invoked by the controller
        self.set_cmd(action)

        (arg_vals, kwarg_vals) = self._prompt_arg_kwarg_vals(op_map[action])

        self.invoke(arg_vals, kwargs=kwarg_vals)

    def exit(self, code):
        sys.exit(code)

    # Gathers the settings for the current package
    def init_settings(self):
        # Check for settings.py for the current package
        if os.path.isfile(f"{PACKAGES_DIR}{self.get_package()}/settings.py") == False:
            # No settings file is found, return an empty SettingSet
            return SettingSet({})

        settings = {}
        # Import the settings
        module = import_module(f"packages.{self.get_package()}.settings", "./")
        settings_attrs = dir(module)
        for attr in settings_attrs:
            # Settings must only contain uppercase letters and underscores
            # and must start with an uppercase letter
            if re.match(rf"{self.settings_pattern}", attr) is not None:
                settings[attr] = getattr(module, attr)

        return SettingSet(settings)

    def _prompt_arg_kwarg_vals(self, method):
        # Get the arg spec for the operation being performed and
        # remove "self" from the arguments
        arg_spec = inspect.getfullargspec(method)
        arg_spec.args.remove("self")

        # Determine the keyword arguments. In the inspect module, the keyword
        # arguments are the last elements of the args list. If there are any,
        # their values will be found in the "defaults" property.
        k_args = []
        if arg_spec.defaults is not None:
            k_args = arg_spec.args[-(len(arg_spec.defaults)):]

        # Determine the positional arguments based on the number of keyword arguments
        pos_args = []
        if len(k_args) > 0:
            pos_args = arg_spec.args[0:-(len(k_args))]
        else:
            pos_args = arg_spec.args
        
        # Prompt the user to provide values for the positional
        arg_vals = []
        for arg in pos_args:
            arg_vals.append(prompt.text(f"{arg}"))

        # Prompt the user to provide values for the keyword arguments
        i = 0
        kwarg_vals = {}
        for arg in k_args:
            kwarg_vals[arg] = prompt.text(
                f"{arg}",
                default=arg_spec.defaults[i],
                # NOTE This may cause some problems somewhere
                # We want to allow users to pass default kwarg values of None.
                # If the default for a givin arg is None, allow nullable
                nullable=(True if arg_spec.defaults[i] == None else False)
            )
            i = i + 1

        return ( arg_vals, kwarg_vals )

    def get_package(self):
        return self.config.get("current", "package")
    
    def get_config(self, key):
        return self.config.get(f"package.{self.get_package()}", key)

    def set_config(self, key, value):
        self.config.add(f"package.{self.get_package()}", key, value)



