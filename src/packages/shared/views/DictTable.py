from typing import Union, Dict, List

from tabulate import tabulate

from core.AbstractView import AbstractView
from typing import Dict


class DictTable(AbstractView):
    """Handles the displaying of data in a table."""
    data: Union[Dict, List]

    def __init__(self, data: Dict):
        self.data = data

    def render(self):
        print(tabulate(self.data.items(), tablefmt="fancy_grid"))
        return
