from typing import List, Dict

from core.Option import Option
from core.OptionSet import OptionSet

from utils.Logger import Logger

class OptionRegistrar:

    option_sets: Dict[str, type[OptionSet]] = {}
    registered_names = []
    registered_aliases = []

    def __init__(self):
        self.option_sets = {}
        self.registered_names = []
        self.registered_aliases = []

    def register(self, controller: str, options: List[type[Option]]) -> None:
        # Do not allow options to be registered for a single controller more than once
        if controller in self.option_sets.keys():
            raise Exception(f"Controller '{controller}' already has registered options")

        self.option_sets[controller] = OptionSet()

        # # Validate the uniqueness of option names and aliases
        for option in options:
            if option.name in self.registered_names:
                raise ValueError(f"Option naming collision: Option already registered with name '{option.name}'")
            if option.name in self.registered_aliases:
                raise ValueError(f"Option naming collision: Alias already exists with the name '{option.name}'")

            self.registered_names.append(option.name)
            
            for alias in option.aliases:
                if alias in self.registered_names:
                    raise ValueError(f"Alias naming collision: Option already registered with name '{alias}'")
                if alias in self.registered_aliases:
                    raise ValueError(f"Alias naming collision: Alias '{alias}' is already registered")
                
            self.registered_aliases = self.registered_aliases + option.aliases
            self.option_sets[controller].add(option)

        # Reset the value of registered names and aliases for each call of the
        # register function
        self.registered_names = []
        self.registered_aliases = []

        return

    def get_option_set(self, controller) -> type[OptionSet]:
        if controller in self.option_sets.keys():
            return self.option_sets[controller]
                
        return self.option_sets["core"]

    # Combine the options of one controller to another. Specific options
    # can be selected by providing a list with the options' name in the
    # options keyword. If strict is set to True, an error will be thrown
    # categories contain duplicate option names. Otherwise, the options 
    # in the to_controller will be overwritten.
    # TODO implement
    def uses(self, to_controller, from_controller, options=[], strict=True):
        pass
