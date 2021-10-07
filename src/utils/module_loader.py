from importlib import import_module
from importlib.util import find_spec

def module_loader(module_name):
    if find_spec(module_name) is not None:
        return import_module(module_name, "./")

    return None

def class_loader(module_name, class_name):

    module = module_loader(module_name)

    if module is not None:
        if hasattr(module, class_name):
            return getattr(module, class_name)

    return None