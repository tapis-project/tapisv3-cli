from typing import List
from core.Option import Option

class OptionSet:
    options: List[type[Option]] = []

    def __init__(self):
        self.options = []

    def add(self, option: type[Option]):
        self.options.append(option)

    def get_names(self) -> List[str]:
        return [option.name for option in self.options]

    def get_by_name(self, name) -> type[Option]:
        for option in self.options:
            if option.name == name:
                return option

        return

    def get_by_context(self, context) -> type[Option]:
        for option in self.options:
            if option.context == context:
                return option

        return