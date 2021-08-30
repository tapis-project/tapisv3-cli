import json

def create(client, system_definition_file) -> None:
    system_definition = json.loads(open(system_definition_file, "r").read())
    client.files.insert(**system_definition)

    return