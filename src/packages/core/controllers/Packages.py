import os, shutil

from core.Controller import Controller
from core.ConfigManager import ConfigManager
from utils.Prompt import prompt
from conf.settings import PACKAGES, PACKAGES_DIR


class Packages(Controller):
    def __init__(self):
        Controller.__init__(self)
        self.conf = ConfigManager()

    def create(self, package_name):
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

    def delete(self, package_name):
        protected_packages = [ "core", "tapis"]
        if package_name in protected_packages:
            raise Exception(f"Error: Cannot delete the following packages: {protected_packages}")

        yn = prompt.yes_no(f"Deleting package '{package_name}' is permanent. Continue? [y/n]")

        if yn:
            package_dir = PACKAGES_DIR + f"/{package_name}/"
            try:
                shutil.rmtree(package_dir)
            except OSError as e:
                self.logger.error(f"{package_dir} : {e.strerror}")
