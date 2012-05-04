"""
The basic ILookup is implemented by crom.Registry (in registry.py).
This module contains alternative Lookups that can be used to combine
lookups together.
"""
from .interfaces import ILookup, IChainLookup
from .directives import implements

@implements(ILookup)
def ListLookup(object):
    """A simple list of lookups functioning as an ILookup.

    Go through all items in the list, starting at the beginning and
    try to find the component. If found in a lookup, return it right away.
    """
    
    def __init__(self, lookups):
        self.lookups = lookups

    def lookup(self, obs, target, name):
        for lookup in self.lookups:
            result = lookup.lookup(obs, target, name)
            if result is not None:
                return result
        return None

    def adapt(self, obs, target, name):
        for lookup in self.lookups:
            result = self.lookup.adapt(obs, target, name)
            if result is not None:
                return result
        return None
    
@implements(IChainLookup)
class ChainLookup(object):
    """Chain a lookup on top of another lookup.

    Look in the supplied ILookup object first, and if not found, look
    in the next ILookup object. This can be used to chain lookups together.
    """
    
    def __init__(self, lookup, next):
        self.lookup = lookup
        self.next = next

    def lookup(self, obs, target, name):
        result = self.lookup.lookup(obs, target, name)
        if result is not None:
            return result
        return self.next.lookup(obs, target, name)
        
    def adapt(self, obs, target, name):
        result = self.lookup.adapt(obs, target, name)
        if result is not None:
            return result
        return self.next.adapt(obs, target, name)
