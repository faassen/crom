from grokker import (Directive, ArgsDirective, grokker, directive)

from zope.interface import Interface

from crom.directives import source, target, name, registry, implements
from crom.grokkers import utility, adapter


# we do want to make adapters automatically get called when used

# traditional naming
#        not called     | called

# 0      utility          null adapter
# 1      context utility  adapter
# n      multi utility    multi adapter

# lookup strategy:

# get the 1, or get a list of all possibilities (subscribers)

# @grokker
# @directive(source)
# @directive(target)
# @directive(name)
# @directive(registry)
# def utility(scanner, name, ob, source, target, name, registry):
#     pass

# there is a list of registries that you can look up in
# alternatively it can use a globally set list of registries to
# look into, this is the equivalent to a site
# @registry can be used to register something with a particular registry
# (only once, I think., or should this be a list?).
# the argument is either a function to look up the registry (found when
# the config action is executed), or an IRegistry object directly.


