from .component import Registry

global_registry = Registry()

def get_current_registry():
    return global_registry

