import options.handlers

from configs import settings
from core.Controller import Controller
from core.Authenticator import Authenticator as Auth

class TapipyController(Controller):
    """
    Handles the parsing and execution of commands specified in the OpenAPI specs.

    Different tools, such as Tapipy, may inherit from this to specify their own
    specific categories and commands.
    """
    operation = None
    resource = None

    def __init__(self):
        Controller.__init__(self)
        try:
            self.client = Auth().authenticate()
            if self.client == None:
                self.exit()
        except SystemExit:
            self.exit()
        except:
            raise ValueError(f"Unable to authenticate user using AUTH_METHOD {settings.AUTH_METHOD}\n")

    def invoke(self, args) -> None:
        """Overwrites the execute method to invoke Tapipy Operations directly."""
        args = self.parse_args(args)
        result = None

        try:
            handlers = { "generic": [], "args": [], "result": [] }
            for option in self.option_set.options:
                # If the current option from the option set has not been provided by the user,
                # ignore it
                if option.name not in self.cmd_options and option.name not in self.arg_options:
                    continue
                
                # If the current option from the option set HAS been provided but there is
                # no handler specified, ignore it
                if option.handler == None or not hasattr(options.handlers, option.handler):
                    continue
                
                # Register the handler
                handlers[option.context].append(getattr(options.handlers, option.handler))
            
            for handler in handlers["generic"]:
                handler(self)

            for handler in handlers["args"]:
                args = handler(self, args)

            # Check that all keyword args for a given operation are
            # present.
            self.validate_kw_args()

            result = self.operation(*args, **self.kw_args)

            for handler in handlers["result"]:
                result = handler(self, result)
            
            if self.view == None:
                self.set_view("TapisResultTableView", result)

            self.view.render()

            return

        except Exception as e:
            self.logger.error(e)

    def set_operation(self, operation_name: str) -> None:
        """Sets the operation to be performed upon execution."""
        self.command = operation_name
        try:
            self.operation = getattr(self.resource, operation_name)
            return
        except:
            self.logger.error(f"{type(self.resource).__name__} has no operation '{operation_name}'\n")
            self.exit(1)

    def set_resource(self, resource_name: str) -> None:
        """Gets the resource name for the OpenAPI command."""
        try:
            self.resource = getattr(self.client, resource_name)
            return
        except:
            self.logger.error(f"{type(self).__name__} has no resource '{resource_name}'\n")
            self.exit(1)

    def validate_kw_args(self):
        """Validates the keyword arguments required by an OpenAPI operation."""
        required_params = []
        for param in self.operation.path_parameters:
            if param.required:
                required_params.append(param.name)

        kw_arg_keys = self.kw_args.keys()
        for param in required_params:
            if param not in kw_arg_keys:
                raise Exception(f"Missing required keyword arguments: {[f'--{param}' for param in required_params if param not in self.kw_args.keys()]}")