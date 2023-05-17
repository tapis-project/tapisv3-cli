from typing import Any

from core.AbstractView import AbstractView


class TapisResultRawView(AbstractView):
    data: Any

    def __init__(self, data):
        self.data = data

    def render(self) -> None:
        print(self.data)

        return
