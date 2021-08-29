from tapipy.errors import InvalidInputError

def undelete(client, system_id) -> None:
    try:
        client.systems.undeleteSystem(systemId=system_id)
        print(f"Recovered system with id '{system_id}'")
        return
    except InvalidInputError:
        print(f"Deleted system not found with id '{system_id}'")
        return
