from tapipy.errors import InvalidInputError

def get(client, system_id) -> None:
    try:
        system = client.systems.getSystem(systemId=system_id)
        print(system)
        return
    except InvalidInputError:
        print(f"Sytem not found with id '{system_id}'")