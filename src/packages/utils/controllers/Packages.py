import os

from shutil import copyfile
from importlib.util import find_spec
from importlib import import_module

from core.BaseController import BaseController
from conf.settings import PACKAGES, PACKAGES_DIR, TEMPLATES_DIR
from utils.Prompt import prompt
from utils.Styles import styler as s 
from utils.Prompt import prompt


class Packages(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.list()

    def create(self):
        package_name = prompt.text("Package name")

        package_dir = PACKAGES_DIR + package_name + "/"
        os.mkdir(package_dir)
        copyfile(f"{TEMPLATES_DIR}files/settings.py", package_dir + "settings.py")
        copyfile(f"{TEMPLATES_DIR}files/aliases.py", package_dir + "aliases.py")
        os.mkdir(package_dir + "controllers/")
        copyfile(f"{TEMPLATES_DIR}controllers/Systems.py", package_dir + "controllers/Systems.py")
        copyfile(f"{TEMPLATES_DIR}controllers/Configure.py", package_dir + "controllers/Configure.py")

        self.logger.complete(f"Package '{package_name}' created.")
        self.configure(package_name=package_name)
        self.logger.info(f"Don't forget to add '{package_name}' to the PACKAGES array in src/conf/settings.py")

    def list(self):
        nl = "\n"
        join_str = f"{nl}- "
        self.logger.log(f"Packages:{nl}- {join_str.join(PACKAGES)}")

    def use(self):
        current_package = self.config.get("current", "package")
        string = f"[{current_package}]"
        answer = prompt.select(
            f"Choose a package {s.muted(string)}",
            PACKAGES,
            sort=True
        )
        self.config.add("current", "package", answer)
        self.logger.complete(f"Using package '{answer}'")

    def configure(self, package_name=None):
        package = package_name
        if package_name == None:
            package = prompt.select("Choose a package to configure", PACKAGES, sort=True)
        
        configure_ns = f"packages.{package}.controllers.Configure"
        has_configure = bool(find_spec(configure_ns))
        if has_configure == False:
            self.logger.warn(f"Package '{package}' has no category 'Configure'")
            return

        module = import_module(configure_ns, "./" )
        if hasattr(module, "Configure") == False:
            self.logger.warn(f"Package '{package}' has no category 'Configure'")
            return

        # Temporarily switch current package to configure this package
        original_package = self.config.get("current", "package")
        self.config.add("current", "package", package)

        configure_controller = getattr(module, "Configure")()
        configure_controller.index()

        # Prompt use to switch to newly configured package
        if original_package != package:
            switch_package = prompt.select(
                f"Switch current package to '{package}'",
                ["yes", "no"]
            )

            # Swtich current package back to the original package
            # if they chooses not to switch
            if switch_package == "no":
                self.config.add("current", "package", original_package)

        self.logger.complete(f"Package '{package}' configured")

        return


