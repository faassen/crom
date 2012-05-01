from zope.interface import providedBy, implementedBy
from zope.interface.interfaces import ISpecification
from zope.interface.adapter import AdapterRegistry
from ._compat import CLASS_TYPES

class InstanceRegistry(object):
    def __init__(self):
        self.registry = AdapterRegistry()

    def register(self, sources, target, name, component):
        iface_sources = []
        for source in sources:
            if ISpecification.providedBy(source):
                iface_sources.append(source)
                continue
            if isinstance(source, CLASS_TYPES):
                iface_sources.append(implementedBy(source))
            else:
                raise TypeError("Sources must either be "
                                "an interface or a class.")
        self.registry.register(iface_sources, target, name, component)

    def lookup(self, obs, target, name):
        return self.registry.lookup(map(providedBy, obs), target, name)

class Registry(object):
    def __init__(self):
        self.utilities = InstanceRegistry()
        self.adapters = InstanceRegistry()

    def register_utility(self, sources, target, name, component):
        self.utilities.register(sources, target, name, component)
        
    def register_adapter(self, sources, target, name, component):
        self.adapters.register(sources, target, name, component)
        
    def get_utility(self, obs, target, name):
        return self.utilities.lookup(obs, target, name)

    def get_adapter(self, obs, target, name):
        adapter = self.adapters.lookup(obs, target, name)
        if adapter is None:
            return None
        return adapter(*obs)

    def get_subscribed(self):
        pass
    
