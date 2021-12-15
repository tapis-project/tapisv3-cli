"""Handlers are the functions associated with the flags passed in on the command line."""

import json
import os


def fileContentsToPositionalArg(controller, args):
    """
    Denotes a file is being passed as an arg via the "-f" flag.
    The file is opened and its contents are used as additional args.
    """
    file_contents = open(controller.arg_options["-f"], "rb").read()
    args.append(file_contents)

    return args


def help(controller):
    """Displays a help message for the specified controller."""
    if hasattr(controller, "help"):
        controller.override_exec = True
        controller.help()
        return

    controller.logger.warn(f"Controller '{type(controller).__name__}' has no help option for the {controller.command} command\n")


def jsonFileToKeywordArgs(controller, args):
    """
    Denotes a JSON file will be converted to keyword args via the "-j" flag.
    The file is opened and its contents are used as keyword args.
    """
    filename = controller.arg_options["-j"]["filename"]
    _, extension = os.path.splitext(filename)

    # Check that the extension of the file is '.json'
    if extension != ".json":
        file_error = "" if os.path.isfile(filename) else f"\nFile '{filename}' does not exist."
        raise Exception(f"Using argument option '-j' requires a valid json file as an argument.{file_error}")

    # Convert the definition file into a json object
    obj = json.loads(open(filename, "r").read())
    for item, value in obj.items():
        controller.kw_args[item] = value

    return args


def resultToFile(controller, result):
    """
    Denotes that the command result should be saved to a file via the "-r" flag.
    The file name specified is where the result will be saved to.
    WARNING: This CAN overwrite file contents if the name of a file that already
    exists is passed in!
    """
    data = result.__str__()

    filename = controller.arg_options["-s"]["filename"]
    with open(filename, "w") as file:
        file.write(data)

    return result


def tapisResultRawView(controller, result):
    """
    Output is not formatted prettily and is displayed
    on the command line exactly how it is returned.
    """
    controller.set_view("TapisResultRawView", result)
    return result


def tapisResultTableView(controller, result):
    """
    Output is formatted cleanly and is displayed in tables
    on the command line rather than raw text.
    """
    controller.set_view("TapisResultTableView", result)
    return result
