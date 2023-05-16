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
                file.write(json.dumps(config))
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

    def create_profile(self, username, base_url, jwt=None):
        config = self.load()
        config["current_user"] = username
        config["current_package"] = settings.DEFAULT_PACKAGE
        config["profiles"].append({"username": username, "base_url": base_url, "jwt": jwt})
        self.write(config)

    def update_profile(self, username, base_url=None, jwt=None):
        profile = self.get_profile(username)
        profile = {
            **profile,
            "base_url": base_url if base_url != None else profile["base_url"],
            "jwt": jwt if jwt != None else profile["jwt"]
        }

        # Get the config, insert the updated profile, and remove the old
        config = self.load()
        modified_profiles = [profile]
        for profile in config["profiles"]:
            if profile["username"] != username:
                modified_profiles.append(profile)

        self.write({**config, "profiles": modified_profiles})

    def delete_profile(self, username):
        config = self.load()
        profiles = list(filter(lambda profile: profile["username"] != username, config["profiles"]))
        self.write({**config, "profiles": profiles})

config_manager = ConfigManager()