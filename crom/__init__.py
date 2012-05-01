from grokker import (Directive, ArgsDirective, grokker, directive)

from zope.interface import Interface

from crom.directives import source, target, name, registry, implements
from crom.grokkers import utility, adapter

from zope.interface.interface import InterfaceClass
from .lookup import adapter_lookup, utility_lookup

from .current import get_current_registry

# # monkey patch instead of adapter hooks mechanism for greater flexibility
InterfaceClass._original_call = InterfaceClass.__call__
InterfaceClass.__call__ = adapter_lookup
InterfaceClass.utility = utility_lookup

