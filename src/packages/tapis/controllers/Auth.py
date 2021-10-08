"""Handles the configuring of credentials."""

from core.Controller import Controller
from core.Configuration import Configuration


class Auth(Controller):
    """Configurations are parsed here."""
    def __init__(self):
        Controller.__init__(self)
        self.config = Configuration()

    def configure(self):
        """Configures the settings to handle input credentials."""
        self.config.configure()
