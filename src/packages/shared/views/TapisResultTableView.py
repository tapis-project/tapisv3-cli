from tabulate import tabulate

from core.AbstractView import AbstractView
# TODO settings should be passed from view contructor, not by importing config manager
from utils.ConfigManager import config_manager


class TapisResultTableView(AbstractView):
    def __init__(self, data, logger=None):
        self.data = data
        self.logger = logger

    def render(self):
        if type(self.data) in [str, int, float]:
            print(self.data)
            return

        if type(self.data) == bytes:
            self.logger.warn("Result is of type 'bytes'. Cannot show result")
            return

        if type(self.data) == dict:
            self.data = [self.data]

        # Get the display settings from the config
        config = config_manager.load()
        settings = config.get("output").get("settings")

        # Truncate the number of colums
        truncated_columns = False
        if (
            len(self.data) > 0
            and len(self.data[0]) >= int(settings.get("max_columns"))
            and int(settings.get("max_columns")) > 0
        ):
            modified_data = []
            for i, _ in enumerate(self.data):
                truncated_columns = True
                modified_data.append(dict(list(self.data[i].items())[0:int(settings.get("max_columns"))]))

            self.data = modified_data


        # Try to make data look nice in table. Convert ojects and lists to "..." and
        # truncate long strings and numbers
        truncated_values = False
        for i, _ in enumerate(self.data):
            for prop in self.data[i]:
                if type(self.data[i][prop]) in [list, dict]:
                    self.data[i][prop] = f"...[{type(self.data[i][prop]).__name__}]"
                elif (
                    type(self.data[i][prop]) in [str, bytes]
                    and len(self.data[i][prop]) >= int(settings.get("max_chars_per_column"))
                    and int(settings.get("max_chars_per_column")) >= 1
                    and prop not in settings.get("never_truncate")
                ):
                    self.data[i][prop] = self.data[i][prop][0:int(settings.get("max_chars_per_column"))] + "..."
                    truncated_values = True
                elif self.data[i][prop] == None:
                    self.data[i][prop] = "null"


        if truncated_values and self.logger != None:
            self.logger.warn(f"Values in the table have been truncated to {settings.get('max_chars_per_column')} characters")

        if truncated_columns and self.logger != None:
            self.logger.warn(f"Only showing the first {settings.get('max_columns')} columns")

        print(tabulate(self.data, headers={}, tablefmt="fancy_grid", showindex=True))
