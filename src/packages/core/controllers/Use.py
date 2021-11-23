from core.BaseController import BaseController
from utils.ConfigManager import configManager as config
from utils.Prompt import prompt
from conf.settings import PACKAGES
from packages.core.controllers.Profile import Profile


class Use(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        answer = prompt.select(
            f"Choose a package",
            PACKAGES
        )
        config.add("current", "package", answer)
        self.logger.complete(f"Using package '{answer}'")

    def package(self):
        self.index()

    def profile(self):
        profile_controller = Profile()
        profile_controller.use()

    
