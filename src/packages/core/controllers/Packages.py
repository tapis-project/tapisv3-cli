import os

from core.BaseController import BaseController
from conf.settings import PACKAGES, PACKAGES_DIR
from utils.Prompt import prompt
from utils.ConfigManager import configManager as config
from utils.Styles import styler as s 


class Packages(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.list()

    def create(self, package_name):
        package_dir = PACKAGES_DIR + package_name + "/"
        os.mkdir(package_dir)
        os.mkdir(package_dir + "controllers/")

    def list(self):
        nl = "\n"
        join_str = f"{nl}- "
        self.logger.log(f"Packages:{nl}- {join_str.join(PACKAGES)}")

    def use(self):
        current_package = config.get("current", "package")
        string = f"[{current_package}]"
        answer = prompt.select_cancel(
            f"Choose a package {s.muted(string)}",
            PACKAGES
        )
        config.add("current", "package", answer)
        self.logger.complete(f"Using package '{answer}'")
