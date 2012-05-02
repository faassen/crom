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

class ILookupChain(ILookup):
    lookup = Attribute("The first ILookup to look in.")
    next = Attribute("The next ILookup in the chain.")

class ILookupStack(ILookup):
    def push(lookup):
        """Push another lookup upon the stack.
        """

    def pop():
        """Pop the top lookup from the stack.

        If the stack only has a single lookup left, raise a
        LookupStackError.
        """

class LookupStackError(IndexError):
    """Raised when trying to pop the base lookup from a ILookupStack
    """

class IRegistry(ILookup):
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
    """API of the current module."""
    def init_registry():
        """Initializes the global registry.

        It can now receive registrations.
        
        This initializes global lookup and registration behavior.

        This means that interface-based lookup lookup behavior
        (``.component``, ``.adapt``, and ``__call__`` if enabled),
        will now work without passing an explicit ``lookup`` argument.

        This also means that the component registration decorators
        will work without having to use the @registry decorator.
        """
        
    def set_registry(registry):
        """Set the global registry to registry.

        Needs to be done once when the application starts up (or use
        ``init_registry``).

        This initializes global lookup and registration behavior.
        
        registry should provide IRegistry.
        """

    def get_registry():
        """Get the global registry.
        """

    def clear_registry():
        """Clear the global registry.

        This disables the global lookup and registration behavior.
        """
        
    def get_lookup():
        """Get the currently set up ILookup instance.
        """
    
    def get_lookup_stack():
        """Get the ILookupStack.

        Can be used to push new ILookup instances onto the stack,
        or pop them again.
        """
    
