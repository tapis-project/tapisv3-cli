import os

from core.Controller import Controller
from core.ConfigManager import ConfigManager
from utils.Prompt import prompt
from conf.settings import PACKAGES, PACKAGES_DIR


class Packages(Controller):
    def __init__(self):
        Controller.__init__(self)
        self.conf = ConfigManager()

    def new(self, package_name):
        package_dir = PACKAGES_DIR + package_name + "/"
        os.mkdir(package_dir)
        os.mkdir(package_dir + "controllers/")


    def use(self):
        package = prompt.validate_choices(
            f"Choose a package: [{'|'.join(PACKAGES)}] ",
            PACKAGES,
            prompt.not_none
        )

        self.conf.add("current", "package", package)

    def list(self):
        nl = "\n"
        join_str = f"{nl}- "
        self.logger.log(f"Packages:{nl}- {join_str.join(PACKAGES)}")
