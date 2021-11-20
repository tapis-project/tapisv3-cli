import packages.shared.options.handlers

from conf import settings
from core.BaseController import BaseController
from packages.tapis.Authenticator import Authenticator as Auth
from helpers.help_formatter import help_formatter as formatter


class TapipyController(BaseController):
    """
    Handles the parsing and execution of commands specified in the OpenAPI specs.

    Different tools, such as Tapipy, may inherit from this to specify their own
    specific categories and commands.
    """
    def __init__(self):
        BaseController.__init__(self)
        self.cmd = None
        self.operation = None
        self.resource = None
        self.operation_ids = []
        try:
            self.client = Auth().authenticate()
            if self.client is None:
                self.exit()
        except SystemExit:
            self.exit()
        except:
            raise ValueError(f"Unable to authenticate user using AUTH_METHOD {settings.AUTH_METHOD}\n")

    def invoke(self, args) -> None:
        """Overwrites the execute method to invoke Tapipy Operations directly."""
        args = self.parse_args(args)
        result = None

        if self.cmd == "help":
            self.set_view("TapisResultRawView", self.operation())
            self.view.render()
            return

        try:
            handlers = { "generic": [], "args": [], "result": [] }
            for option in self.option_set.options:
                # If the current option from the option set has not been provided by the user,
                # ignore it
                if option.name not in self.cmd_options and option.name not in self.arg_options:
                    continue

                # If the current option from the option set HAS been provided but there is
                # no handler specified, ignore it
                if option.handler == None or not hasattr(packages.shared.options.handlers, option.handler):
                    continue

                # Register the handler
                handlers[option.context].append(getattr(packages.shared.options.handlers, option.handler))
            
            for handler in handlers["generic"]:
                handler(self)

            for handler in handlers["args"]:
                args = handler(self, args)

            # Check that all keyword args for a given operation are
            # present.
            self._validate_kw_args()

            result = self.operation(*args, **self.kw_args)

            for handler in handlers["result"]:
                result = handler(self, result)

            if self.view is None:
                self.set_view("TapisResultTableView", result)

            self.view.render()

            return

        except Exception as e:
            self.logger.error(e)

    def _help(self):
        formatter.add_usage(f"$tapis {self.resource.resource_name} [options] [command] [args/keyword args]")

        for operation_id in self.operation_ids:
            op = getattr(self.resource, operation_id)
            formatter.add_command(
                operation_id,
                keyword_args=[param.name for param in op.path_parameters]
            )

        formatter.add_options(self.option_set.options)
        
        return formatter.build()

    def set_resource(self, resource_name: str) -> None:
        """Gets the resource for the OpenAPI command."""
        try:
            self.resource = getattr(self.client, resource_name)
        except:
            self.logger.error(f"{type(self).__name__} has no category '{resource_name}'\n")
            self.exit(1)

        for _, path_desc in self.resource.resource_spec.items():
            for _, op_desc in path_desc.operations.items():
                self.operation_ids.append(op_desc.operation_id)

    def set_operation(self, operation_name: str) -> None:
        """Sets the operation to be performed upon execution."""
        self.cmd = operation_name
        
        if operation_name == "help":
            self.operation = self._help
            return

        try:
            self.operation = getattr(self.resource, operation_name)
            return
        except:
            self.logger.error(f"Category '{self.resource.resource_name}' has no command '{operation_name}'\n")
            self.logger.log(self._help())
            self.exit(1)

    def _validate_kw_args(self):
        """Validates the keyword arguments required by an OpenAPI operation."""
        required_params = []
        if hasattr(self.operation, "path_parameters"):
            for param in self.operation.path_parameters:
                if param.required:
                    required_params.append(param.name)

        kw_arg_keys = self.kw_args.keys()
        for param in required_params:
            if param not in kw_arg_keys:
                raise Exception(f"Missing required keyword arguments: {[f'--{param}' for param in required_params if param not in self.kw_args.keys()]}")
