from core.BaseController import BaseController
from conf.settings import PACKAGES
from utils.Prompt import prompt
from utils.Styles import styler as s 
from utils.Prompt import prompt


class Packages(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.list()

    def list(self):
        nl = "\n"
        join_str = f"{nl}- "
        self.logger.log(f"Packages:{nl}- {join_str.join(PACKAGES)}")

    def use(self):
        current_package = self.config_manager.get_current_package()
        string = f"[{current_package}]"
        package = prompt.select(
            f"Choose a package {s.muted(string)}",
            PACKAGES,
            sort=True
        )
        self.config_manager.set_current_package(package)
        self.logger.complete(f"Using package '{package}'")