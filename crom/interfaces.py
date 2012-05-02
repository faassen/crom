from zope.interface import Interface

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
    
