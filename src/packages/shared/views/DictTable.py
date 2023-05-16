from typing import Union, Dict, List

from tabulate import tabulate

from core.AbstractView import AbstractView
from typing import Dict


class DictTable(AbstractView):
    """Handles the displaying of data in a table."""
    data: Union[Dict, List]

    def __init__(self, data: Dict, headers=[]):
        self.data = data
        self.headers = headers

    def render(self):
        print(tabulate(self.data, headers=self.headers, tablefmt="fancy_grid"))
