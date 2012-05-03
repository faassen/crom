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

class ICurrent(Interface):
    """The current global registry and lookup.

    The current can be set up once when the application starts up, by calling
    setup().

    You can also do a custom setup during startup by setting the
    registry attribute to some IRegistry instance yourself. You will
    also need to set up the lookup attribute in this case.
    
    If not set up, the current will contain a implementations of
    IRegistry and ILookup which will raise exceptions when you try to
    register or look up.

    During runtime you can vary what will be used to look up
    components by modifying the lookup attribute. This lookup
    attribute is managed separately per thread.

    The ChainLookup can be used for instance to wrap the registry
    in another one, thereby installing another lookup strategy.

    Once the registry is set up, the component registration decorators
     will work without having to use the @registry decorator.

    Once the lookup is set up, interface-based lookup lookup behavior
    (``.component``, ``.adapt``, and ``__call__`` if enabled), will
    now work without passing an explicit ``lookup`` argument.
    """

    registry = Attribute("IRegistry")
    lookup = Attribute("ILookup")

    def setup():
        """Set up a standard registry and lookup.
        """

    def teardown():
        """Clears the currently set registry and lookup. Make it failing again.
        """
