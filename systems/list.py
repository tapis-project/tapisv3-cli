from tapipy.tapis import Tapis
import sys

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]

# Authenticate
client = Tapis(base_url= "https://tacc.develop.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def list_systems() -> None:
    systems = client.systems.getSystems()
    if len(systems) > 0:
        for system in systems:
            print(system.id)
        return

    print(f"No systems found for user '{tacc_username}'")
    return

if __name__ == "__main__":
    list_systems()
