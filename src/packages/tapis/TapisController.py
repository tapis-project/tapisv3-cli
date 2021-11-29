import inspect

from tapipy.tapis import Tapis

from core.BaseController import BaseController
from packages.tapis.Authenticator import Authenticator as Auth
from utils.Prompt import prompt


class TapisController(BaseController):
    """Base Tapis Controller."""
    client: type[Tapis]

    def __init__(self):
        BaseController.__init__(self)

    def before(self):
        try:
            self.client = Auth().authenticate()
            if self.client is None:
                self.exit(1)
        except SystemExit:
            self.exit(1)
        except:
            raise ValueError(f"Unable to authenticate user")

    def index(self):
        self.select_Action()

    # TODO add tab autocomplete for files and dirs
    def select_Action(self) -> None:
        # Get the methods for this controller and remove the select_Action
        methods = self.get_methods()
        methods.remove("select_Action")

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

        # Get the arg spec for the operation being performed and
        # remove "self" from the arguments
        arg_spec = inspect.getfullargspec(op_map[action])
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
            arg_vals.append(prompt.not_none(f"{arg}"))

        # Prompt the user to provide values for the keyword arguments
        i = 0
        kwarg_vals = {}
        for arg in k_args:
            kwarg_vals[arg] = prompt.not_none(f"{arg}", default=arg_spec.defaults[i])
            i = i + 1

        self.invoke(arg_vals, kwargs=kwarg_vals)
        
