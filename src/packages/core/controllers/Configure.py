import os

from core.BaseController import BaseController
from utils.ConfigManager import ConfigManager
import conf.settings as settings


class Configure(BaseController):
    def __init__(self):
        BaseController.__init__(self)
        self.conf = ConfigManager()

    def index(self):
        # If the configs.ini specified in the settings does not exist,
        # create it.
        if not os.path.isfile(settings.CONFIG_FILE):
            self.logger.log(f"Creating config file '{settings.CONFIG_FILE}'\n")
            self.conf.create_config_file()