import os
from shutil import copyfile

from core.BaseController import BaseController
from conf.settings import PACKAGES, PACKAGES_DIR, TEMPLATES_DIR
from utils.Prompt import prompt
from utils.ConfigManager import configManager as config
from utils.Styles import styler as s 
from utils.Prompt import prompt


class Packages(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.list()

    def create(self, *args):
        if len(args) > 1:
            package_name = args[0]
        else:
            package_name = prompt.text("Package name")

        package_dir = PACKAGES_DIR + package_name + "/"
        os.mkdir(package_dir)
        copyfile(f"{TEMPLATES_DIR}files/settings.py", package_dir + "settings.py")
        copyfile(f"{TEMPLATES_DIR}files/aliases.py", package_dir + "aliases.py")
        os.mkdir(package_dir + "controllers/")
        copyfile(f"{TEMPLATES_DIR}controllers/Example.py", package_dir + "controllers/Example.py")

        self.logger.complete(f"Package '{package_name}' created.")
        self.logger.info(f"Don't forget to add '{package_name}' to the PACKAGES array src/conf/settings.py")

    def list(self):
        nl = "\n"
        join_str = f"{nl}- "
        self.logger.log(f"Packages:{nl}- {join_str.join(PACKAGES)}")

    def use(self):
        current_package = config.get("current", "package")
        string = f"[{current_package}]"
        answer = prompt.select(
            f"Choose a package {s.muted(string)}",
            PACKAGES
        )
        config.add("current", "package", answer)
        self.logger.complete(f"Using package '{answer}'")
