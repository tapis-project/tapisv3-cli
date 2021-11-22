from core.BaseController import BaseController
from utils.ConfigManager import ConfigManager
from utils.Prompt import prompt
from conf.settings import PACKAGES


class Use(BaseController):
    def __init__(self):
        BaseController.__init__(self)
        self.conf = ConfigManager()

    def index(self):
        answer = prompt.select(
            f"Choose a package:",
            PACKAGES
        )
        self.conf.add("current", "package", answer)
        self.logger.complete(f"Using package '{answer}'")

    
