from grokker import (Directive, ArgsDirective, grokker, directive)

from zope.interface import Interface
from zope.interface.interfaces import ComponentLookupError

from crom.directives import sources, target, name, registry, implements
from crom.grokkers import component, adapter

from .current import get_current
from .config import grok, configure

# we do the absolutely compatible monkey patches , not breaking
# the __call__ behavior of interface in any possible way as we don't touch it
# to change the __call__ behavior use crom.monkey.compat() instead (or in
# addition)
from . import monkey
monkey.safe()
