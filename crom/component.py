from zope.interface import providedBy
from zope.interface.adapter import AdapterRegistry

class InstanceRegistry(object):
    def __init__(self):
        self.registry = AdapterRegistry()

    def register(self, sources, target, name, component):
        self.registry.register(sources, target, name, component)

    def lookup(self, obs, target, name):
        return self.registry.lookup(map(providedBy, obs), target, name)

class Registry(object):
    def __init__(self):
        self.utilities = InstanceRegistry()
        self.adapters = InstanceRegistry()
        
                 
def get_utility_for_provided(target, provided):
    """Get the utility identified by the interface target.

    Provided is a description of 0..n classes or interfaces that
    function as the source.
    """
    pass

def get_utility(target, obs):
    return get_utility_for_provided(target, provided(obs))
    
def get_adapter(target, obs):
    return get_utility(target, obs)(*obs)
    

