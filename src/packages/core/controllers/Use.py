from core.BaseController import BaseController
from packages.core.controllers.Profiles import Profiles
from packages.core.controllers.Packages import Packages


class Use(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.package()

    def package(self):
        packages_controller = Packages()
        packages_controller.use()

    def profile(self):
        profile_controller = Profiles()
        profile_controller.use()

    
