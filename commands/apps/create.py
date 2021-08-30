import json

def create(client, definition_file) -> None:
    definition = json.loads(open(definition_file, "r").read())
    client.apps.createAppVersion(**definition)

    return