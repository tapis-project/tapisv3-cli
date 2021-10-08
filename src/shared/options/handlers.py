import os, json

def fileContentsToPositionalArg(controller, args):
    file_contents = open(controller.arg_options["-f"], "rb").read()
    args.append(file_contents)

    return args

def help(controller):
    if hasattr(controller, "help"):
        controller.override_exec = True
        controller.help()
        return
    
    controller.logger.warn(f"controller '{type(controller).__name__}' has no help option for the {controller.command} command")

def jsonFileToKeywordArgs(controller, args):
    filename = controller.arg_options["-j"]["filename"]
    _, extension = os.path.splitext(filename)
    
    # Check that the extension of the file is '.json'
    if extension != ".json":
        raise Exception(f"Using argument option '-j' requires a json file argument. Provided: '{extension}'")
    
    # Convert the definition file into a json object
    obj = json.loads(open(filename, "r").read())
    for item, value in obj.items():
        controller.kw_args[item] = value
    
    return args

def resultToFile(controller, result):
    data = result.__str__()

    filename = controller.arg_options["-s"]["filename"]
    with open(filename, "w") as file:
        file.write(data)

    return result

def tapisResultRawView(controller, result):
    controller.set_view("TapisResultRawView", result)
    return result

def tapisResultTableView(controller, result):
    controller.set_view("TapisResultTableView", result)
    return result
