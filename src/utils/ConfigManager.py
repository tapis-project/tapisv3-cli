import json

from conf import settings
from utils.Logger import Logger


class ConfigManager:
    def __init__(self):
        self.logger = Logger()

    def load(self):
        with open(settings.CONFIG_FILE, "r") as file:
            try:
                return json.loads(file.read())
            except json.JSONDecodeError as e:
                self.logger.error(f"Bad configuation file: {settings.CONFIG_FILE} - {e}")

    def write(self, config):
         with open(settings.CONFIG_FILE, "w") as file:
            try:
                file.write(json.dumps(config, indent=2))
            except Exception as e:
                self.logger.error(f"Error writing to config file: {e}")

    def get_current_user(self):
        return self.load()["current_user"]

    def set_current_user(self, username):
        config = self.load()
        config["current_user"] = username
        self.write(config)

    def get_current_package(self):
        return self.load()["current_package"]

    def get_current_login(self, username):
        profile = self.get_profile(username)

        if profile == None:
            return None

        return {
            "username": profile["username"],
            "base_url": profile["current_base_url"],
            "jwt": next(filter(lambda auth: auth["base_url"] == profile["current_base_url"], profile["auths"]), {}).get("jwt", None)
        }

    def set_current_package(self, package):
        config = self.load()
        config["current_package"] = package
        self.write(config)

    def get_profile(self, username):
        config = self.load()
        profile = next(filter(lambda profile: profile["username"] == username, config["profiles"]), None)
        return profile

    def list_profiles(self):
        config = self.load()
        return config["profiles"]

    def create_profile(self, profile):
        config = self.load()
        config["current_user"] = profile.get("username")
        config["current_package"] = settings.DEFAULT_PACKAGE
        config["profiles"].append(profile)
        self.write(config)

    def update_profile(self, profile):
        # Get the config, insert the updated profile and remove the old
        config = self.load()
        modified_profiles = [profile]
        for existing_profile in config["profiles"]:
            if existing_profile["username"] != profile["username"]:
                modified_profiles.append(existing_profile)

        self.write({**config, "profiles": modified_profiles})

    def delete_profile(self, username):
        config = self.load()
        profiles = list(filter(lambda profile: profile["username"] != username, config["profiles"]))
        self.write({**config, "profiles": profiles})

config_manager = ConfigManager()