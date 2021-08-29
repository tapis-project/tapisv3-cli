def list(client) -> None:
    apps = client.apps.getApps()
    if len(apps) > 0:
        for app in apps:
            print(app.id)
        return

    print(f"No apps found for user 'xxx'")
    return