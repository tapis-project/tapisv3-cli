from typing import Union, Dict, List

from tabulate import tabulate

from core.AbstractView import AbstractView


class TapisResultTableView(AbstractView):
    """Handles the displaying of data in a table."""
    data: Union[Dict, List]

    def __init__(self, data):
        self.data = data

    def render(self):
        """The data is prettified and displayed neatly in tables on the command line."""
        if type(self.data) == list:
            for _, item in enumerate(self.data):
                print(tabulate(vars(item).items(), tablefmt="fancy_grid"))
            return
            
        print(tabulate(vars(self.data).items(), ["Key", "Value"], tablefmt="fancy_grid"))

        return
