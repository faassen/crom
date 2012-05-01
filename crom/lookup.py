from zope.interface.interfaces import ComponentLookupError
from .current import get_current_registry

SENTINEL = object()

def lookup(iface, lookup_func, utility_or_adapter, *args, **kw):
    sources = args
    target = iface
    name = kw.pop('name', '')
    default = kw.pop('default', SENTINEL)
    component = lookup_func(sources, target, name)
    
    if component is not None:
        return component
    if default is not SENTINEL:
        return default
    raise ComponentLookupError(
        "Could not find %s from sources %s to target %s." %
        (utility_or_adapter, sources, target))

# iface will serve as 'self' when monkey-patched onto InterfaceClass
def component_lookup(iface, *args, **kw):
    registry = kw.pop('registry', None)
    #if registry is None:
    #    registry = get_current_registry()
    return lookup(iface, registry.lookup, 'component', *args, **kw)

def adapter_lookup(iface, *args, **kw):
    # shortcut bail out necessary to make this work without known registry
    if len(args) == 1 and iface.providedBy(args[0]):
        return args[0]
    registry = kw.pop('registry', None)
    return lookup(iface, registry.get_adapter, 'adapter', *args, **kw)

