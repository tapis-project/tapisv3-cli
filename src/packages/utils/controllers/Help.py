import sys

from importlib import import_module

from core.BaseController import BaseController
from utils.Styles import styler as s
from utils.ConfigManager import config_manager


class Help(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def index(self):
        self.logger.log(s.underline("\nGeneral utilities"))
        self.logger.log(f"{s.blue('shell')} - Starts a tapis shell that enables users to run multiple commands directly to the cli API in a single process (cannot run nested shells)")
        self.logger.log(f"{s.blue('login')} - Authenticates with a Tapis deployment and creates user profile")
        self.logger.log(f"{s.blue('profile')} - List, remove, and switch to different user profiles")
        self.logger.log(f"{s.blue('packages')} - List and switch between packages")
        self.logger.log(f"{s.blue('set')} - Modify cli output type and output directory for file output types")
        self.logger.log(f"{s.blue('info')} - Show current user, packages, and auth info")

        # Get current package
        package = config_manager.get_current_package()
        
        self.logger.info(f"Generating help info...")
        self.logger.log(s.underline(f"\nPackage Specific Commands for the '{package}' package"))
        try:
            # Import the current package's settings module
            settings_module = import_module(f"packages.{package}.settings", "./" )
            HELP = getattr(settings_module, "HELP", {})
        except Exception as e:
            self.logger.error(f"Package Error: {e}")
            sys.exit(1)

        help_controller = HELP.get("controller", None)
        help_method = HELP.get("method", None)

        if help_controller == None or help_method == None:
            self.logger.warn(f"Package '{package}' has not implemented help functionality")

        try:
            # Import the current package's settings module
            module = import_module(f"packages.{package}.controllers.{help_controller}", "./" )
            ControllerClass = getattr(module, help_controller)
            controller = ControllerClass()
            method = getattr(controller, help_method)
            method()
        except Exception as e:
            self.logger.error(f"Package Error: {e}")
            sys.exit(1)


    
