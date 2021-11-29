from typing import Any

from core.AbstractView import AbstractView


class TapisResultRawView(AbstractView):
    """Handles the displaying of raw data."""
    data: Any

    def __init__(self, data):
        self.data = data

    def render(self) -> None:
        """Prints the raw data to the command line."""
        print(self.data)

        return
