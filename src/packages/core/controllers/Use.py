from core.BaseController import BaseController
from utils.ConfigManager import ConfigManager
from utils.Prompt import prompt
from conf.settings import PACKAGES


class Use(BaseController):
    def __init__(self):
        BaseController.__init__(self)
        self.conf = ConfigManager()

    def index(self):
        package = prompt.validate_choices(
            f"Choose a package: [{'|'.join(PACKAGES)}] ",
            PACKAGES,
            prompt.not_none
        )

        self.conf.add("current", "package", package)

    
