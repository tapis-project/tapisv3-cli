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

    def _build_config(self, tenant, instance):
        config = f"config.{tenant}.{instance}.jhub"
        if self.config_type == "group":
            config = f"{self.group}.group." + config

        return config

