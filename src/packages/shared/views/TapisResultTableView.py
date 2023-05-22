from typing import Union, Dict, List

from tabulate import tabulate

from core.AbstractView import AbstractView


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

        # Truncate the number of colums if over 8
        truncated_columns = False
        if len(self.data) > 0 and len(self.data[0]) >= 8:
            modified_data = []
            for i, _ in enumerate(self.data):
                truncated_columns = True
                modified_data.append(dict(list(self.data[i].items())[0:8]))

            self.data = modified_data


        # Try to make data look nice in table. Convert ojects and lists to "..." and
        # truncate long strings and numbers
        truncated_values = False
        for i, _ in enumerate(self.data):
            for prop in self.data[i]:
                if type(self.data[i][prop]) in [list, dict]:
                    self.data[i][prop] = "..."
                elif type(self.data[i][prop]) in [str, bytes] and len(self.data[i][prop]) >= 16:
                    self.data[i][prop] = self.data[i][prop][-13:] + "..."
                    truncated_values = True
                elif self.data[i][prop] == None:
                    self.data[i][prop] = "null"


        if truncated_values and self.logger != None:
            self.logger.warn("Values in the table have been truncated to 13 chars for readability")

        if truncated_columns and self.logger != None:
            self.logger.warn("Only showing the first 8 columns")

        print(tabulate(self.data, headers={}, tablefmt="fancy_grid", showindex=True))
