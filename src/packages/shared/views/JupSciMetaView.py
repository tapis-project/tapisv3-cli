from typing import Union, Dict, List

from tabulate import tabulate

from core.AbstractView import AbstractView
from typing import Dict


class JupSciMetaView(AbstractView):
    """Handles the displaying of data in a table."""
    data: Union[Dict, List]

    def __init__(self, data: Dict):
        self.data = data

    def render(self):
        if type(self.data) == list:
            for item in self.data:
                self.render_data(item)
            return

        self.render_data(self.data)

    def render_data(self, data):
        value = data.pop("value")
        print("Result")
        print(tabulate(data.items(), tablefmt="fancy_grid"))
        print("Value")
        print(tabulate(value.items(), tablefmt="fancy_grid"))

