from core.BaseController import BaseController
from utils.Prompt import prompt
from utils.ConfigManager import config_manager


class Display(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    def settings(self):
        config = config_manager.load()

        max_columns = prompt.text(
            "Maximum # of columns to display in table view (int)",
            default=config.get("output").get("settings").get("max_columns"),
            value_type=int
        )

        max_chars_per_column = prompt.text(
            "Maximum # of characters per column (int)",
            default=config.get("output").get("settings").get("max_chars_per_column"),
            value_type=int
        )

        default_never_truncate = ",".join(config.get("output").get("settings").get("never_truncate"))
        never_truncate = prompt.text(
            "List of properties exempt from trunction (comma-seperated list of strings)",
            default=default_never_truncate,
        )
        never_truncate = never_truncate.replace(" ", "").split(",")

        first_column = prompt.text(
            "Column name to show first tables: Ex: 'id', 'uuid', 'jobUuid'",
            default=config.get("output").get("settings").get("first_column"),
            value_type=str
        )

        config["output"]["settings"] = {
            "max_columns": max_columns,
            "max_chars_per_column": max_chars_per_column,
            "never_truncate": never_truncate,
            "first_column": first_column
        }

        config_manager.write(config)

        self.logger.complete(f"Display settings updated")