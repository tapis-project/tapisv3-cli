from packages.tapis.TapisController import TapisController
from utils.Prompt import prompt

class JupSciController(TapisController):
    def __init__(self):
        TapisController.__init__(self)
        self.config_type = "tenant"
        self.group = None

    def before(self):
        TapisController.before(self)
        self.config_type = prompt.select(
            "Choose a config type",
            ["tenant", "group"]
        )

        if self.config_type == "group":
            self.group = prompt.text("group")
        

