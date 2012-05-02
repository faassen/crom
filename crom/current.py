from .registry import Registry, LookupChain
from .directives import implements
from .interfaces import ILookupStack, LookupStackError, ICurrent
from zope.interface.declarations import moduleProvides

moduleProvides(ICurrent)

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

def init_registry():
    set_registry(Registry())
    
def set_registry(registry):
    global global_registry
    global_registry = registry
    _set_lookup_stack(registry)

def clear_registry():
    global_lookup = None
    global_registry = None
    
def get_lookup_stack():
    return global_lookup_stack

get_lookup = get_lookup_stack

def _set_lookup_stack(lookup):
    global global_lookup_stack
    global_lookup_stack = LookupStack(lookup)

global_lookup_stack = None
global_registry = None
