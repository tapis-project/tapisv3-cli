from core.BaseController import BaseController
from packages.tapis.settings import ENVS
from utils.Prompt import prompt
from packages.utils.controllers.Profiles import Profiles

class Configure(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        profile_controller = Profiles()
        profile_controller.add()

        # Set env and tenant
        env = prompt.select("Tapis Env", ENVS)
        self.config.add("package.tapis", "env", env)

        tenant = prompt.select("Tapis Tenant", [ "tacc" ])
        self.config.add("package.tapis", "tenant", tenant)

        # Set the current package to tapis
        self.config.add("current", "package", "tapipy")

        return
    