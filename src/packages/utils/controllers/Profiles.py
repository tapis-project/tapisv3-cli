from core.BaseController import BaseController
from utils.Prompt import prompt
from conf.settings import AUTH_METHODS, PASSWORD
from core.AuthCredential import AuthCredential
from utils.Styles import styler as s

class Profiles(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.list()

    def use(self):
        current_profile = self.config.get("current", "profile")
        string = s.muted(f"[{current_profile}]")
        profiles = self.config.get_section_keys("profiles")
        profile = prompt.select(f"Choose a profile {string}", profiles)
        self.config.add("current", "profile", profile)

        self.logger.complete(f"Using profile '{profile}'")

    def add(self):
        self.logger.log("Create a new profile")
        # Prompt the username to create a username and password
        username = prompt.text("Username")
        if self.config.has_key(f"profiles", username):
            self.logger.error(f"'{username}' is already a configured profile")
            self.exit(1)

        self.config.add("profiles", username, "enabled")
        self.config.add_section(f"profile.{username}")

        auth_method = prompt.select("Choose an authentication method", AUTH_METHODS)

        credential = None
        if auth_method == PASSWORD:
            password = prompt.text("Password 🔒", secret=True)
            credential = AuthCredential(password=password)

        self.config.add(f"current", "profile", username)
        self.config.add(f"profile.{username}", "auth_method", auth_method)
        
        for item, value in credential.__dict__.items():
            if value is not None:
                self.config.add(f"profile.{username}", item, value)

    def list(self):
        profiles = self.config.get_section_keys("profiles")
        self.set_view("ListItems", profiles)
        self.view.render()

    
