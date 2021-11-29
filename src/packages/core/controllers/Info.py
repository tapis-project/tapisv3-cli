from core.BaseController import BaseController
from utils.ConfigManager import configManager as config


class Info(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.set_view("DictTable", {
            "Profile": config.get("current", "profile"),
            "Package": config.get("current", "package"),
            "Auth method": config.get("current", "auth_method")
        })
        self.view.render()