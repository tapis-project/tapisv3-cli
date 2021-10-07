from tabulate import tabulate

from typing import Union, Dict, List

from core.AbstractView import AbstractView

class TapisResultTableView(AbstractView):
    data: Union[Dict, List]

    def __init__(self, data):
        self.data = data
        
    def render(self):
        if type(self.data) == list:
            for _, item in enumerate(self.data):
                print(tabulate(vars(item).items(), tablefmt="fancy_grid"))
            
            return

        print(tabulate(vars(self.data).items(), ["Key", "Value"], tablefmt="fancy_grid"))

        return