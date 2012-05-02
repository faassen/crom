from .registry import Registry, LookupChain
from .directives import implements
from .interfaces import ILookupStack, LookupStackError

@implements(ILookupStack)
class LookupStack(object):
    def __init__(self, registry):
        self.lookup = LookupChain(registry, None)

    def lookup(self, obs, target, name):
        return self.lookup.lookup(obs, target, name)

    def adapt(self, obs, target, name):
        return self.lookup.adapt(obs, target, name)

    def push(self, lookup):
        self.lookup = LookupChain(lookup, self.lookup)

    def pop(self):
        if self.lookup.next is None:
            raise StackableRegistryError("Cannot pop last registry.")
        self.lookup = self.lookup.next

def get_registry():
    return global_registry

def set_registry(registry):
    global global_registry
    global_registry = registry
    set_lookup(registry)

def clear_registry():
    global_lookup = None
    global_registry = None
    
def get_lookup():
    return global_lookup

def set_lookup(lookup):
    global global_lookup
    global_lookup = LookupStack(lookup)

global_lookup = None
global_registry = None
