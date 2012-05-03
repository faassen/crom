from zope.interface.interfaces import ComponentLookupError
from .current import current

SENTINEL = object()

def do_lookup(iface, lookup_func, component_name, *args, **kw):
    sources = args
    target = iface
    name = kw.pop('name', '')
    default = kw.pop('default', SENTINEL)
    if kw:
        raise TypeError("Illegal extra keyword arguments: %s" %
                        ', '.join(kw.keys()))
    component = lookup_func(sources, target, name)
    
    if component is not None:
        return component
    if default is not SENTINEL:
        return default
    raise ComponentLookupError(
        "Could not find %s from sources %s to target %s." %
        (component_name, sources, target))

def find_lookup(kw):
    lookup = kw.pop('lookup', None)
    if lookup is None:
        lookup = current.lookup
    return lookup

# iface will serve as 'self' when monkey-patched onto InterfaceClass
def component_lookup(iface, *args, **kw):
    return do_lookup(
        iface, find_lookup(kw).lookup, 'component', *args, **kw)

def adapter_lookup(iface, *args, **kw):
    # a shortcut rule to make sure self-adaption works even without
    # a registry supplied
    if len(args) == 1 and iface.providedBy(args[0]):
        return args[0]
    return do_lookup(
        iface, find_lookup(kw).adapt, 'adapter', *args, **kw)

