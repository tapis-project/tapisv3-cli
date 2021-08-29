from importlib import import_module

class CommandResolver:

    def resolve(self, args: list) -> None:
        module = import_module( f"modules.{args[0]}.{args[1]}", "./" )
        return getattr(module, args[1])