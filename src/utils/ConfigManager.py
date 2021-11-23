import os

from configparser import ConfigParser

from conf import settings
from utils.Logger import Logger
from conf.templates.core import template


class ConfigManager:
    """
    Manages the setting, getting, and checking of all package-based configs
    """
    auth_method: str
    config: ConfigParser
    credentials: dict
    package: str

    def __init__(self):
        # Intialize and set the configparser to the Configuration object and
        # get the credentials from the config file.
        self.auth_method = settings.AUTH_METHOD
        self.parser = ConfigParser()
        self.parser.read(settings.CONFIG_FILE)
        self.logger = Logger()
        self.package = None
        self.credentials = {}

        # Add the credentials from the config file to 
        # this Configuration object's credentials dict.
        if "credentials" in self.parser.sections():
            for key in self.parser["credentials"]:
                self.credentials[key] = self.parser["credentials"][key]

    def create_config_file(self):
        head, _ = os.path.split(settings.CONFIG_FILE)
        os.makedirs(head)
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

    def get_section(self, section):
        return self.parser.items(section)

    def get_section_keys(self, section):
        items = self.get_section(section)
        return [item[0] for item in items]

    def get_section_values(self, section):
        items = self.get_section(section)
        return [item[1] for item in items]

    def has_section(self, section):
        return section in self.parser.sections()
    
    def has_key(self, section, key):
        return (self.has_section(section) and key in self.parser[section])
                
    def get(self, section, key):
        return self.parser[section][key]

configManager = ConfigManager()