from zope.interface import Interface
from zope.interface.interfaces import ComponentLookupError

from .registry import Registry
from .lookup import ListLookup, ChainLookup

from .directives import sources, target, name, registry, implements
from .grokkers import component, adapter

from .current import current
setup = current.setup
teardown = current.teardown

from .config import grok, configure

# we do the absolutely compatible monkey patches , not breaking
# the __call__ behavior of interface in any possible way as we don't touch it
# to change the __call__ behavior use crom.monkey.compat() instead (or in
# addition)
from . import monkey
monkey.safe()

__all__ = ["Interface", "ComponentLookupError",
           "Registry", "ListLookup", "ChainLookup",
           "sources", "target", "name", "registry", "implements",
           "component", "adapter",
           "current", "setup", "teardown", "grok", "configure"]

