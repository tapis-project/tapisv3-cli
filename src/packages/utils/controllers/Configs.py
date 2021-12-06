from core.BaseController import BaseController
from utils.ConfigManager import configManager as config


class Configs(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def set(self, key, value):
        section = config.get("current", "package")
        config.add(section, key, value)
        self.logger.complete(f"Config updated: {section}.{key}")

    
