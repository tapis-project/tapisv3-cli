from typing import Union, Dict, List
from core.AbstractView import AbstractView


class QuietView(AbstractView):
    """Handles the displaying of data in a table."""
    data: Union[Dict, List]

    def __init__(self, data):
        self.data = data

    def render(self):
        """The data is prettified and displayed neatly in tables on the command line."""
        if type(self.data) == list:
            for _, item in enumerate(self.data):
                if hasattr(item, "id"):
                    print(item.id)
                    continue

                if hasattr(item, "__dict__") and "id" in self.data:
                    print(item["id"])
                    continue
            return
        
        if hasattr(self.data, "__dict__"):
            print(vars(self.data)["id"])
            return
        
        print(self.data)

        return
