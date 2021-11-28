from core.BaseController import BaseController
from packages.core.controllers.Profiles import Profiles
from packages.core.controllers.Packages import Packages
from utils.ConfigManager import configManager as config
from utils.Prompt import prompt
from packages.tapis.settings import ENVS


class Use(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.profile()
        self.package()
        self.tenant()
        self.env()

    def package(self):
        packages_controller = Packages()
        packages_controller.use()

    def profile(self):
        profile_controller = Profiles()
        profile_controller.use()

    def env(self):
        env = prompt.select("Tapis Env", ENVS)
        config.add("package.tapis", "env", env)

    def tenant(self):
        tenant = prompt.select("Tapis Tenant", [ "tacc" ])
        config.add("package.tapis", "tenant", tenant)

    
