from tapipy.errors import InvalidInputError

def delete(client, system_id, path) -> None:
    try:
        client.files.delete(systemId=system_id, path=path)
        print(f"Deleted file '{path}' in system '{system_id}'")
        return
    except InvalidInputError:
        print(f"File '{path}' not found in system '{system_id}'")
        return