from configparser import ConfigParser

from conf import settings
from utils.Logger import Logger
from conf.templates.core import template


class ConfigManager:
    """
    Writes user credentials to the configs.ini based on the AUTH_METHOD 
    provided in the settings.py file.
    """
    auth_method: str = settings.AUTH_METHOD
    config: ConfigParser = None
    credentials: dict = {}

    def __init__(self):
        # Intialize and set the configparser to the Configuration object and
        # get the credentials from the config file.
        self.parser = ConfigParser()
        self.parser.read(settings.CONFIG_FILE)
        self.logger = Logger()

        # Add the credentials from the config file to 
        # this Configuration object's credentials dict.
        if "credentials" in self.parser.sections():
            for key in self.parser["credentials"]:
                self.credentials[key] = self.parser["credentials"][key]

    def create_config_file(self):
        for key, val in template.items():
            self.parser[key] = val
            with open(settings.CONFIG_FILE, "w") as file:
                self.parser.write(file)

    def add(self, section, key, value):
        self.parser[section][key] = value
        with open(settings.CONFIG_FILE, "w") as file:
            self.parser.write(file)

    def add_section(self, section, overwrite=True):
        if section not in self.parser.sections():
            self.parser[section] = {}
            with open(settings.CONFIG_FILE, "w") as file:
                self.parser.write(file)

    def has_section(self, section):
        if section in self.parser.sections():
            return True

        return False

    def get(self, section, key):
        return self.parser[section][key]