"""Allows the user to look at and query the available options."""

from typing import List

from core.Option import Option


class OptionSet:
    """Options can either be listed altogether or queried by some context."""
    options: List[type[Option]] = []

    def __init__(self):
        self.options = []

    def add(self, option: type[Option]):
        """Adds an option to the option set."""
        self.options.append(option)

    def get_names(self) -> List[str]:
        """Lists the names of all available options."""
        return [option.name for option in self.options]

    def get_by_name(self, name) -> type[Option]:
        """An option can be queried by its option name."""
        for option in self.options:
            if option.name == name:
                return option

        return None

    def get_by_context(self, context) -> type[Option]:
        """An option can be queried by a property other than its name."""
        for option in self.options:
            if option.context == context:
                return option

        return None
