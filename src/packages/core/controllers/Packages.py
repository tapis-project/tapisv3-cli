import os, shutil

from core.BaseController import BaseController
from utils.Prompt import prompt
from conf.settings import PACKAGES, PACKAGES_DIR


class Packages(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def create(self, package_name):
        package_dir = PACKAGES_DIR + package_name + "/"
        os.mkdir(package_dir)
        os.mkdir(package_dir + "controllers/")

    def list(self):
        nl = "\n"
        join_str = f"{nl}- "
        self.logger.log(f"Packages:{nl}- {join_str.join(PACKAGES)}")

    def delete(self, package_name):
        protected_packages = ["core", "tapis", "tapipy"]
        if package_name in protected_packages:
            raise Exception(f"Error: Cannot delete the following packages: {protected_packages}")

        yn = prompt.yes_no(f"Deleting package '{package_name}' is permanent. Continue? [y/n]")

        if yn:
            package_dir = PACKAGES_DIR + f"/{package_name}/"
            try:
                shutil.rmtree(package_dir)
            except OSError as e:
                self.logger.error(f"{package_dir} : {e.strerror}")
