from core.BaseController import BaseController
from packages.utils.controllers.Profiles import Profiles
from packages.utils.controllers.Packages import Packages


class Use(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.profile()
        self.package()

    def package(self):
        packages_controller = Packages()
        packages_controller.use()

    def profile(self):
        profile_controller = Profiles()
        profile_controller.use()

    
