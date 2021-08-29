from tapipy.errors import InvalidInputError

def delete(client, id) -> None:
    try:
        client.apps.deleteApp(appId=id)
        print(f"Deleted app with id '{id}'")
        return
    except InvalidInputError:
        print(f"App not found with id '{id}'")
        return