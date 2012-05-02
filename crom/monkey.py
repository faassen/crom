from zope.interface.interface import InterfaceClass
from lookup import component_lookup, adapter_lookup

def safe():
    InterfaceClass.component = component_lookup
    InterfaceClass.adapt = adapter_lookup

def incompat():
    safe()
    # monkey patch instead of adapter hooks mechanism as we change
    # the call signature
    InterfaceClass._original_call = InterfaceClass.__call__
    InterfaceClass.__call__ = adapter_lookup

def revert_safe():
    del InterfaceClass.component
    del InterfaceClass.adapt
    
def revert_incompat():
    revert_safe()
    InterfaceClass.__call__ = InterfaceClass._original_call
    del InterfaceClass._original_call
    
