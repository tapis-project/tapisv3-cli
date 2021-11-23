import os

from core.BaseController import BaseController
from utils.ConfigManager import configManager as config
import conf.settings as global_settings
from packages.tapis.settings import ENVS
from utils.Prompt import prompt
from packages.core.controllers.Profile import Profile

class Configure(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        profile_controller = Profile()

        # Prompt user for username and password
        self.logger.log("Tacc credentials not found.")
        prompt.yes_no("Create credentials? [y/n]: ")

        profile_controller.add()

        # Set env and tenant
        env = prompt.select("Tapis Env: ", ENVS)
        config.add("tapis", "env", env)

        tenant = prompt.select("Tapis Tenant", [ "tacc" ])
        config.add("tapis", "tenant", tenant)

        # Set the current package to tapis
        config.add("current", "package", "tapis")

        return
    