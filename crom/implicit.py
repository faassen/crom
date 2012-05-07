import threading
from .registry import Registry
from .directives import implements
from .interfaces import IImplicit

@implements(IImplicit)
class Implicit(object):
    def __init__(self):
        self._registry = None
        self.local = threading.local()

    def initialize(self):
        self.initialize_with_registry(Registry())

    def initialize_with_registry(self, registry):
        self._registry = registry
        self.local.lookup = registry

    def clear(self):
        self._registry = None
        self.local.lookup = None

    @property
    def registry(self):
        return self._registry

    @property
    def base_lookup(self):
        return self.registry
        
    @property
    def lookup(self):
        return self.local.lookup

    @lookup.setter
    def lookup(self, value):
        self.local.lookup = value

    def reset_lookup(self):
        self.lookup = self.base_lookup

implicit = Implicit()

    
