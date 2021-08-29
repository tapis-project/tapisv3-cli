from tapipy.errors import InvalidInputError

def delete(client, system_id) -> None:
    try:
        client.systems.deleteSystem(systemId=system_id)
        print(f"Deleted system with id '{system_id}'")
        return
    except InvalidInputError:
        print(f"System not found with id '{system_id}'")
        return