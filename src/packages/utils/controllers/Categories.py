import os

from core.BaseController import BaseController
from utils.Styles import styler as s
from conf.settings import PACKAGES_DIR


class Categories(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.list()

    def list(self):
        core_walk = os.walk(f"{PACKAGES_DIR}/core/controllers/")
        controller_files = [ d for d in core_walk ][0][2]
        
        self.logger.log(s.underline(f"Package: {s.bold('core')}"))
        
        for controller_file in controller_files:
            controller = controller_file.replace(".py", "").lower()
            self.logger.log(controller)

        self.logger.newline(1)

        package = self.config.get("current", "package")

        if package == "tapipy":
            self.exit(0)

        package_walk = os.walk(f"{PACKAGES_DIR}{package}/controllers")
        controller_files = [ d for d in package_walk ][0][2]

        self.logger.log(s.underline(f"Package: {s.bold(package)}"))

        for controller_file in controller_files:
            controller = controller_file.replace(".py", "").lower()
            self.logger.log(controller)

        self.logger.newline(1)



        



        

    
