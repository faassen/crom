from .registry import Registry

global_registry = Registry()

def get_current():
    return global_registry

