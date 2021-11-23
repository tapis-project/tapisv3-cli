from typing import Union, Dict, List

from tabulate import tabulate

from core.AbstractView import AbstractView
from typing import List


class ListItems(AbstractView):
    """Handles the displaying of data in a table."""
    data: Union[Dict, List]

    def __init__(self, data: List):
        self.data = data

    def render(self):
        for item in self.data:
            print(item)
        return
