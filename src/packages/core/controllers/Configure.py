import os

from core.BaseController import BaseController
from utils.ConfigManager import configManager as config
import conf.settings as settings


class Configure(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        # If the configs.ini specified in the settings does not exist,
        # create it.
        if not os.path.isfile(settings.CONFIG_FILE):
            self.logger.log(f"Creating config file '{settings.CONFIG_FILE}'\n")
            config.create_config_file()