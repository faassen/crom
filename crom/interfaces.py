from zope.interface import Interface, Attribute

class ILookup(Interface):
    def lookup(obs, target, name):
        """Look up a component in the registry.

        obs is a list of 0 to n objects that we use to look up the component.
        If multiple obs are listed, the look up is made for that combination
        of obs. The classes and/or interfaces of the objects are used
        to do the look up.

        The target is the interface that we want to look up. The
        component found should normally provide that interface, although
        no such checking is done and in some situations, such as
        when this is used for adapter lookup, it won't.

        The name the name under which the component should be looked
        up. If the component has not been registered under that name,
        it won't be found.
        
        If the component can be found, it will be returned. If the
        component cannot be found, ``None`` is returned.
        """
        
    def adapt(obs, target, name):
        """Look up an adapter in the registry. Adapt obs to target interface.

        The behavior of this method is like that of lookup, but it
        performs an extra step: it calls the found component with the
        obs given as arguments. The resulting instance should provide
        the target interface (although no such checking is done).
        """

class IChainLookup(ILookup):
    lookup = Attribute("The first ILookup to look in.")
    next = Attribute("The next ILookup in the chain.")

class IRegistry(Interface):
    def register(sources, target, name, component):
        """Register a component with the registry.

        sources is a list of 0 to n interfaces or classes that
        the component is registered for. If multiple sources are listed,
        a registration is made for that combination of sources.

        The target is an interface by which the component can be
        looked up.  The registered object should either provide that
        interface directly, or in the case of an adapter, produce an
        instance that provides that interface when called.

        The name the name under which the component should be
        registered. This can be used to distinguish different
        registrations from each other.
        
        The component is a python object (function, class, instance) that is
        registered.
        """

class ICromInterface(Interface):
    pass

class IImplicit(Interface):
    """Implicit global registry and lookup.

    Crom supports an implicit registry and lookup to be set up
    globally.  Registration of components using grokkers will use the
    implicit global IRegistry instance for registration. Lookups using
    the ICromInterface extension to interface will use the global
    ILookup instance.

    The global registry is normally only set up once per application,
    during startup time. It can be set up to the default crom registry
    using the initialize method. This also sets up a lookup for this
    registry. Afterwards, the registry can be accessed through the
    ``registry`` property (but cannot be set through this).

    In addition to the implicit global registry, an application can
    also use explicit registry objects. The registry to use can be set
    explicitly per registration, using the @registry decorator when
    registering a component using a grokker.
    
    The global implicit lookup can be accessed through the ``lookup``
    property. The global implicit lookup is used in the ICromInterface
    extensions to Interface to look up components. If you don't want
    to use the global implicit lookup with this API, you can pass an
    explicit ``lookup`` argument instead.
    
    Changing the implicit lookup during run-time is done by simply
    assigning to it. Typically you'd assign an ILookup constructed
    using crom.ListLookup or crom.ChainLookup. This way a lookup can
    look for a component in one registry first, and then fall back to
    another registry, etc.

    To change the lookup back to a lookup in the global implicit
    registry, call ``reset_lookup``.
    
    The implicit lookup is thread-local: each thread has a separate
    implicit global lookup.
    """

    registry = Attribute("IRegistry. Read-only.")
    lookup = Attribute("ILookup. Can be assigned")
    base_lookup = Attribute("ILookup based on IRegistry")
    
    def initialize():
        """Set up a standard global implicit registry and lookup.
        """

    def initialize_with_registry(registry):
        """Set up global implicit registry and lookup according to argument.
        """

    def clear():
        """Clear global implicit registry and lookup.
        """

    def reset_lookup():
        """Reset global implicit lookup to base_lookup.
        """
   
class NoImplicitRegistryError(Exception):
    pass

class NoImplicitLookupError(Exception):
    pass

