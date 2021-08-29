from tapipy.errors import InvalidInputError

def submit(client, name, id, version) -> None:
    try:
        client.jobs.submitJob(name=name, appId=id, appVersion=version)
        return
    except InvalidInputError as e:
        print(e.message)