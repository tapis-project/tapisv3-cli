import json

from json.decoder import JSONDecodeError

import packages.shared.options.handlers

from core.BaseController import BaseController
from core.enums import OutputEnum
from packages.tapis.Authenticator import Authenticator as Auth
from packages.tapis.utils import serialize_result
from helpers.help_formatter import help_formatter as formatter
from utils.Prompt import prompt
from utils.ConfigManager import config_manager
from utils.open_api.type_transformer import TRANSFORMS, transform
from utils.Styles import styler as s


class TapipyController(BaseController):
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
        except Exception as e:
            raise ValueError(f"Unable to authenticate user: {e}")

    def index(self):
        return self._select_Action()

    def invoke(self, args) -> None:
        if self.cmd == "help":
            self.set_view("TapisResultRawView", self.operation())
            self.view.render()
            return

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

            # Pass all keyword arguments to the Tapipy operation as "request_body"
            # instead of unpacking the keyword arguments in the operation call.
            # NOTE If we unpack the keyword arguments directly in the operation call,
            # none of the data will be passed to the API for all operations that have a
            # request body that contains anyOf, allOf, or oneOf objects.
            if self.resource.resource_name in ["workflows"]:
                self.kw_args = { "request_body": self.kw_args }

            result = self.operation(*args, **self.kw_args)
            
            for handler in handlers["result"]:
                result = handler(self, result)
            
            # Get the output type from the config
            config = config_manager.load()

            if config["output"]["type"] == OutputEnum.JSONFile.value:
                result = serialize_result(result)
                self.set_view(
                    "JSONFileView",
                    result,
                    config["output"]["dir"],
                    filename_prefix = self.resource.resource_name + "." + self.operation.operation_id,
                    logger=self.logger
                )
            elif config["output"]["type"] == OutputEnum.File.value:
                self.set_view(
                    "FileView",
                    result,
                    config["output"]["dir"],
                    filename_prefix = self.resource.resource_name + "." + self.operation.operation_id,
                    logger=self.logger)
            elif config["output"]["type"] == OutputEnum.Raw.value:
                self.set_view("TapisResultRawView", result)
            elif config["output"]["type"] == OutputEnum.Table.value:
                serialized_result = serialize_result(result)
                self.set_view("TapisResultTableView", serialized_result, logger=self.logger)
            elif config["output"]["type"] == OutputEnum.JSON.value:
                serialized_result = serialize_result(result)
                self.set_view("TapisResultJSONView", serialized_result, logger=self.logger)
            else:
                self.set_view("TapisResultRawView", result)

            self.view.render()

        except Exception as e:
            self.logger.error(e)

    def _help(self):
        formatter.add_usage(f"$tapis {self.resource.resource_name} [options] [command] [args/keyword args]")

        for operation_id in self.operation_ids:
            op = getattr(self.resource, operation_id)
            required_keyword_args = [ param["name"] for param in op.path_parameters ]
            optional_keyword_args = []
            
            # Populate required keyword args for request body
            required_props = []
            if op.request_body.get("required", False):
                for mime_type in op.request_body.get("content").keys():
                    required_props += op.request_body.get("content").get(mime_type).get("schema").get("required", [])
                required_keyword_args = (
                    required_keyword_args
                    + [ prop for prop in required_props ]
                )
            
            # Populate optional keyword args from request body
            content = op.request_body.get("content", None)
            if content != None:
                optional_props = []
                for mime_type in content.keys():
                    props = content[mime_type].get("schema").get("properties", {})
                    optional_props += [
                        prop for prop in props.keys()
                        if prop not in required_props
                    ]

                optional_keyword_args = (
                    optional_keyword_args
                    + [ prop for prop in optional_props ]
                )
                
            # List all query parameters as keyword arguments
            if hasattr(op, "query_parameters"):
                required_keyword_args = (
                    required_keyword_args + 
                    [ qp["name"] for qp in op.query_parameters if qp.get("required", False) ]
                )

                optional_keyword_args = (
                    optional_keyword_args + 
                    [ qp["name"] for qp in op.query_parameters if not qp.get("required", False) ]
                )

            formatter.add_command(
                operation_id,
                required_keyword_args=required_keyword_args,
                optional_keyword_args=optional_keyword_args
            )

        formatter.add_options(self.option_set.options)
        
        return formatter.build()

    def _resources_help(self):
        from tapipy.tapis import RESOURCES
        self.logger.log(f"{s.underline('Interactive mode')}")
        self.logger.log("Run `$tapis` in a shell (or when in a tapis shell, just press the `enter/return` key) and you will be prompted to choose an api and operation to run")
        self.logger.log(f"\n{s.underline('Manual mode')}")
        self.logger.log(f"{s.underline('Usage')} $tapis [api] [operation_id]")
        self.logger.log(f"{s.underline('Example')} $tapis system getSystems --systemId my-system-id")
        self.logger.log("\n")
        for resource_name in RESOURCES["tapipy"]:
            self.logger.log(f"{s.blue(resource_name)} - run operations on the Tapis {resource_name.capitalize()} API ")
        self.logger.log("\n")
        
    def set_resource(self, resource_name: str) -> None:
        """Gets the resource for the OpenAPI command."""
        try:
            # TODO Remove once files resource fully implements insert operation
            # and removes the upload method
            if resource_name == "upload":
                raise Exception()

            self.resource = getattr(self.client, resource_name)
        except:
            self.logger.error(f"{type(self).__name__} has no category '{resource_name}'\n")
            self.exit(1)

        for _, path_desc in self.resource.resource_spec.items():
            for _, op_desc in path_desc.items():
                self.operation_ids.append(op_desc["operationId"])

    def set_operation(self, operation_name: str) -> None:
        """Sets the operation to be performed"""
        self.cmd = operation_name
        
        if operation_name == "index":
            self.operation = self.index
            return

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
        # Path parameters
        if hasattr(self.operation, "path_parameters"):
            for param in self.operation.path_parameters:
                if param.get("required", False):
                    required_params.append(param["name"])

        # Query parameters
        if hasattr(self.operation, "query_parameters"):
            for param in self.operation.query_parameters:
                if param.get("required", False):
                    required_params.append(param["name"])

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

    # Prompts the user to select an operation id from a drop down, then
    # prompts them the input values for the required keyword arguments
    def _select_Action(self) -> None:
        # Generate a dictionary where the key is the operation_id
        # and the value is the method attr itself
        op_map = {}
        for operation_name in self.operation_ids:
            op_map[operation_name] = getattr(self.resource, operation_name)

        # Prompt the user to select a cmd(operation) to perform
        cmd = prompt.select("Select an operation", [ op for op, _ in op_map.items() ], sort=True)

        # Prompt user to provide values for the path parameters. The key and 
        # value of these will be used as keyword arguments
        kw_args = {}
        params = [ param for param in op_map[cmd].path_parameters ]
        len(params) > 0 and self.logger.log("Path parameters:")
        for param in params:
            kw_args[param["name"]] = prompt.text(f"{param['name']}", required=param.get("required", False))

        # Prompt user to provide values for the query parameters
        qps = [ qp for qp in op_map[cmd].query_parameters ]
        len(qps) > 0 and self.logger.log("Query parameters:")

        for qp in qps:
            qp_value = prompt.text(f"{qp['name']}", required=qp.get("required", False))

            # Only add the query parameters as keyword args to tapipy if there is a value provided
            if qp_value != None:
                kw_args[qp["name"]] = qp_value
        
        # If the current operation requires a request body, prompt the user
        # to choose a method to satisfy that request body
        request_body = op_map[cmd].request_body
        method = None
        JSON_FILE = "provide a json file"
        # EACH = "prompt for each property"
        EDITOR = "build request body in an editor"
        if request_body.get("required", False):
            self.logger.log("This operation requires a request body")
            method = prompt.select(f"Choose a method",
                [
                    JSON_FILE,
                    # EACH,
                    EDITOR,
                ]
            )

        args = []
        if method == JSON_FILE:
            args = self._prompt_json_file()
        elif method == EDITOR:
            obj = self._prompt_editor("Create a request body")
            kw_args = {**kw_args, **{ key:value for key, value in obj}}
        # elif method == EACH:
        #     # Prompt the user for each individual property 
        #     request_body_kw_args = self._prompt_request_body(request_body)
        #     kw_args = { **kw_args, **request_body_kw_args }

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
        
    # # Iterates through the request body and prompts the user for a value
    # # based on the type of value it expect. The prompt values are then transformed
    # # from a string to their correct type and stored in kw_args
    # def _prompt_request_body(self, request_body):
    #     properties = request_body.content["application/json"].schema.properties
    #     required_props = request_body.content["application/json"].schema.required
    #     kw_args = {}
    #     self.logger.debug(properties.values)
    #     for prop, desc in properties.items():
    #         # Prompt for primitive types
    #         if desc.type.value in TRANSFORMS["primitives"]:
    #             required = prop in required_props
    #             kw_args[prop] = self._prompt_primitives(prop, desc, required=required)
    #             continue
            
    #         kw_args[prop] = self._prompt_editor(prop)

    #     return kw_args

    def _prompt_primitives(self, prop, desc, required=False):
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
                required=required,
                value_type=TRANSFORMS["primitives"][desc.type.value]
            )

            # Transform the open api schema type into the correct
            # python type
            return transform(desc.type.value, value)

    


    



        
