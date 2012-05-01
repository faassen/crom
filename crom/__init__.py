from grokker import (Directive, ArgsDirective, grokker, directive)

from zope.interface import Interface
from zope.interface.interfaces import ComponentLookupError

from crom.directives import source, target, name, registry, implements
from crom.grokkers import component, adapter

from . import monkey

from .current import get_current_registry

# we do the absolutely compatible monkey patches first, not breaking
# the __call__ behavior of interface in any possible way as we don't touch it
# to change the __call__ behavior use .monkey.compat() instead
monkey.safe()
