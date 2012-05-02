from zope.interface import providedBy, implementedBy
from zope.interface.interfaces import ISpecification
from zope.interface.adapter import AdapterRegistry
from ._compat import CLASS_TYPES
from .interfaces import IRegistry, ILookup, ILookupChain
from .directives import implements

@implements(IRegistry)
class Registry(object):
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

    def adapt(self, obs, target, name):
        # self-adaptation
        if len(obs) == 1 and target.providedBy(obs[0]):
            return obs[0]
        adapter = self.lookup(obs, target, name)
        if adapter is None:
            return None
        try:
            return adapter(*obs)
        except TypeError, e:
            raise TypeError(str(e) + " (%s)" % adapter)

@implements(ILookupChain)
class LookupChain(object):    
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
