from core.BaseController import BaseController
from utils.ConfigManager import configManager as config
from packages.jupyterscinco.controllers.Set import Set


# NOTE This is a special controller. It cannot be accessed via the command line
# except through `tapis package configure`. If you added your package to the
# PACKAGES array in main settings.py, you can select your package and it will
# run the index method on this controller
class Configure(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    # NOTE Do not remove this method. Doing so will result in unexpected behavior.
    # Use this method to set configs specific to your package using the ConfigManager
    # instance(config)
    def index(self):
        if config.has_section(f"package.{self.get_package()}") == False:
            config.add_section(f"package.{self.get_package()}")

        set_controller = Set()
        method_names = set_controller.get_methods()
        
        for method_name in method_names:
            method = getattr(set_controller, method_name)
            (arg_vals, kwarg_vals) = self._prompt_arg_kwarg_vals(method)
            method(*arg_vals, **kwarg_vals)

        

