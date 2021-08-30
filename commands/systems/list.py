def list(client) -> None:
    systems = client.systems.getSystems()
    if len(systems) > 0:
        for system in systems:
            print(system.id)
        return

    print(f"No systems found for user 'xxx'")
    return
