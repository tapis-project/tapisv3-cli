from tapipy.errors import InvalidInputError

def get(client, id) -> None:
    try:
        app = client.apps.getApp(appId=id)
        print(app)
        return
    except InvalidInputError:
        print(f"App not found with id '{id}'")