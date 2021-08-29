from tapipy.errors import InvalidInputError

def undelete(client, app) -> None:
    try:
        client.apps.undeleteApp(appId=id)
        print(f"Recovered app with id '{id}'")
        return
    except InvalidInputError:
        print(f"Deleted app not found with id '{id}'")
        return