from core.Controller import Controller
from core.ConfigManager import ConfigManager


class Auth(Controller):
    """Configurations are parsed here."""
    def __init__(self):
        Controller.__init__(self)
        self.config = ConfigManager()

    def configure(self):
        """Configures the settings to handle input credentials."""
        self.config.configure()
