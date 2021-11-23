from core.BaseController import BaseController
from utils.ConfigManager import configManager as config
from utils.Prompt import prompt
from conf.settings import AUTH_METHODS, PASSWORD
from core.AuthCredential import AuthCredential


class Profile(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def use(self):
        profiles = config.get_section_keys("profiles")
        profile = prompt.select("Choose a profile", profiles)
        config.add("current", "profile", profile)

        self.logger.complete(f"Using profile '{profile}'")

    def add(self):
        self.logger.log("Create a new profile")
        # Prompt the username to create a username and password
        username = prompt.not_none("Username: ")
        if config.has_key(f"profiles", username):
            self.logger.error(f"'{username}' is already a configured profile")
            self.exit(1)

        config.add("profiles", username, "enabled")
        config.add_section(f"profile.{username}")

        auth_method = prompt.select("Choose an authentication method", AUTH_METHODS)

        credential = None
        if auth_method == PASSWORD:
            password = prompt.not_none("Password 🔒:", secret=True)
            credential = AuthCredential(password=password)

        config.add(f"profile.{username}", "auth_method", auth_method)
        
        for item, value in credential.__dict__.items():
            if value is not None:
                config.add(f"profile.{username}", item, value)

    def list(self):
        pass

    
