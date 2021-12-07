from core.BaseController import BaseController
from utils.ConfigManager import configManager as config

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
        pass
    