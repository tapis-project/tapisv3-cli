import os

from core.Controller import Controller
from utils.ConfigManager import ConfigManager
import conf.settings as settings


class Setup(Controller):
    def __init__(self):
        Controller.__init__(self)
        self.conf = ConfigManager()

    def init(self):
        # If the configs.ini specified in the settings does not exist,
        # create it.
        if not os.path.isfile(settings.CONFIG_FILE):
            self.logger.log(f"Creating config file '{settings.CONFIG_FILE}'\n")
            self.conf.create_config_file()