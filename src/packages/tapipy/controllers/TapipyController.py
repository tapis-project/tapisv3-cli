import json

from json.decoder import JSONDecodeError

import packages.shared.options.handlers

from conf import settings
from core.BaseController import BaseController
from packages.tapis.Authenticator import Authenticator as Auth
from helpers.help_formatter import help_formatter as formatter
from utils.Prompt import prompt
from utils.open_api.type_transformer import TRANSFORMS, transform


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
                self.exit(1)
        except SystemExit:
            self.exit(1)
        except:
            raise ValueError(f"Unable to authenticate user using AUTH_METHOD {settings.AUTH_METHOD}\n")

    def index(self):
        return self._select_Action()

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
            keyword_args = [param.name for param in op.path_parameters]
            
            if hasattr(op.request_body, "required"):
                keyword_args.append("request_body")

            # List all query parameters as keyword arguments
            if hasattr(op, "query_parameters"):
                keyword_args = (keyword_args + 
                    [qp.name for qp in op.query_parameters if qp.required == True])

            formatter.add_command(
                operation_id,
                keyword_args=keyword_args
            )

        formatter.add_options(self.option_set.options)
        
        return formatter.build()

    def set_resource(self, resource_name: str) -> None:
        """Gets the resource for the OpenAPI command."""
        try:
            # TODO Remove once files resource fully implements insert operation
            # Add convenience upload method to operation_ids for files
            if resource_name == "upload":
                raise Exception()
            self.resource = getattr(self.client, resource_name)
        except:
            self.logger.error(f"{type(self).__name__} has no category '{resource_name}'\n")
            self.exit(1)

        for _, path_desc in self.resource.resource_spec.items():
            for _, op_desc in path_desc.operations.items():
                self.operation_ids.append(op_desc.operation_id)

    def set_operation(self, operation_name: str) -> None:
        """Sets the operation to be performed"""
        self.cmd = operation_name
        
        if operation_name == "index":
            self.operation = self.index
            return

        if operation_name == "help":
            self.operation = self._help
            return

        # TODO Remove once files resource fully implements insert operation
        # Set the operation to the convenience function
        if operation_name == "upload" and self.resource.resource_name == "files":
            self.operation = self._upload
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
        # Path parameters
        if hasattr(self.operation, "path_parameters"):
            for param in self.operation.path_parameters:
                if param.required:
                    required_params.append(param.name)
                    
        # Query parameters
        if hasattr(self.operation, "query_parameters"):
            for param in self.operation.query_parameters:
                if param.required:
                    required_params.append(param.name)

        kw_arg_keys = self.kw_args.keys()
        for param in required_params:
            if param not in kw_arg_keys:
                raise Exception(f"Missing required keyword arguments: {[f'--{param}' for param in required_params if param not in self.kw_args.keys()]}")

    # TODO Remove once the insert operation on the files resource is fully supported
    # by Tapipy
    def _upload(self, system_id, path_to_file, destination_folder) -> None:
        try:
            self.client.upload(
                system_id = system_id,
                source_file_path = path_to_file,
                dest_file_path = destination_folder
            )
            return f"Uploaded file '{path_to_file}' to {destination_folder}\n"
        except Exception as e:
            self.logger.error(f"{e.message}\n")
            self.exit(1)

    # TODO add tab autocomplete for files and dirs
    # Prompts the user to select an operation id from a drop down, then
    # prompts them the input values for the required keyword arguments
    def _select_Action(self) -> None:
        # Generate a dictionary where the key is the operation_id
        # and the value is the method attr itself
        op_map = {}
        for operation_name in self.operation_ids:
            op_map[operation_name] = getattr(self.resource, operation_name)

        # Prompt the user to select a cmd(operation) to perform
        cmd = prompt.select("Perform action", [ op for op, _ in op_map.items() ], sort=True)

        # Prompt user to provide values for the path parameters. The key and 
        # value of these will be used as keyword arguments
        kw_args = {}
        params = [param for param in op_map[cmd].path_parameters]
        len(params) > 0 and self.logger.log("Path parameters:")
        for param in params:
            kw_args[param.name] = prompt.text(f"{param.name}", required=param.required)

        # Prompt user to provide values for the query parameters
        qps = [ qp for qp in op_map[cmd].query_parameters ]
        len(qps) > 0 and self.logger.log("Query parameters:")
        for qp in qps:
            kw_args[qp.name] = prompt.text(f"{qp.name}", required=qp.required)

        # If the current operation requires a request body, prompt the user
        # to choose a method to satisfy that request body
        request_body = op_map[cmd].request_body
        method = None
        JSON_FILE = "provide a json file"
        EACH = "prompt for each property"
        EDITOR = "build request body in an editor"
        if hasattr(request_body, "required"):
            self.logger.log("This operations requires a request body")
            method = prompt.select(f"Choose a method",
                [
                    JSON_FILE,
                    EACH,
                    EDITOR,
                ]
            )

        args = []
        if method == JSON_FILE:
            args = self._prompt_json_file()
        elif method == EDITOR:
            obj = self._prompt_editor("Create a request body")
            kw_args = {**kw_args, **{ key:value for key, value in obj}}
        elif method == EACH:
            # Prompt the user for each individual property 
            request_body_kw_args = self._request_body_prompt(
                request_body.content["application/json"].schema.properties)
            kw_args = { **kw_args, **request_body_kw_args }
           

        return (cmd, kw_args, args)

    # Returns -j arg with the value of the json file chosen by the user
    def _prompt_json_file(self):
        # Prompt the user to provide a json definition.
        json_definition_file = prompt.text(f"json file")

        # Add a the "-j" cmd_option to the args along with its value
        return [ "-j", json_definition_file ]

    def _prompt_editor(self, message):
        try:
            contents = prompt.editor(message)
            return json.loads(contents).items()
        except AttributeError:
            self.logger.error("Request body must be a valid JSON object")
            self._prompt_editor(message)
        except JSONDecodeError:
            self.logger.error("The request body contains invalid JSON")
            self._prompt_editor(message)
        
    # Iterates through the request body and prompts the user for a value
    # based on the type of value it expect. The prompt values are then transformed
    # from a string to their correct type and stored in kw_args
    def _request_body_prompt(self, properties):
        kw_args = {}
        for prop, desc in properties.items():
            # Prompt for primitive types
            if desc.type.value in TRANSFORMS["primitives"]:
                kw_args[prop] = self._prompt_primitives(prop, desc)
                continue
            
            kw_args[prop] = self._prompt_editor(prop)

        return kw_args

    def _prompt_primitives(self, prop, desc):
        # Handle booleans
        if desc.type.value == "boolean":
            # Returns boolean so no need to transform the type
            return prompt.select_bool(
                prop, 
                description=f"type: {desc.type.value}"
            )
        # Handle enums
        elif hasattr(desc, "enum") and desc.enum is not None:
            value = prompt.select(
                prop,
                desc.enum,
                description=f"type: enum[{desc.type.value}]"
            )

            return transform(desc.type.value, value)
        # Handle non-boolean primitives
        else:
            value = prompt.text(
                prop,
                description=f"type: {desc.type.value}",
                value_type=TRANSFORMS["primitives"][desc.type.value]
            )

            # Transform the open api schema type into the correct
            # python type
            return transform(desc.type.value, value)



        
