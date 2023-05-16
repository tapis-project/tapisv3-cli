import os, json

from configparser import ConfigParser

from conf import settings
from utils.Logger import Logger


class ConfigManager:
    """
    Manages the setting, getting, and checking of all package-based configs
    """
    auth_method: str
    config: ConfigParser
    package: str

    def __init__(self):
        self.parser = ConfigParser()
        # self.parser.read(settings.CONFIG_FILE)
        self.logger = Logger()
        self.package = None

    def add(self, section, key, value):
        self.parser[section][key] = value
        with open(settings.CONFIG_FILE, "w") as file:
            self.parser.write(file)

    def add_section(self, section, overwrite=True):
        if section not in self.parser.sections():
            self.parser[section] = {}
            with open(settings.CONFIG_FILE, "w") as file:
                self.parser.write(file)

    def get_section(self, section):
        return dict(self.parser.items(section))

    def get_section_keys(self, section):
        items = self.get_section(section).items()
        return [key for key, _ in items]

    def get_section_values(self, section):
        items = self.get_section(section).items()
        return [value for _, value in items]

    def has_section(self, section):
        return section in self.parser.sections()
    
    def has_key(self, section, key):
        return (self.has_section(section) and key in self.parser[section])

    def remove_entry(self, section, key):
        if self.has_key(section, key):
            profiles = self.get_section(section)
            del profiles[key]
            self.parser.remove_section(section)
            self.add_section(section)
            for key, value in profiles.items():
                self.add(section, key, value)
            
    def get(self, section, key):
        if self.has_key(section, key):
            return self.parser[section][key]
        return None

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