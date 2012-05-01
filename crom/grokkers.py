from grokker import grokker, directive
from .directives import source, target, name, registry

@grokker
@directive(source)
@directive(target)
@directive(name)
@directive(registry)
def component(scanner, pyname, obj, source, target, name, registry):
    pass

@grokker
@directive(source)
@directive(target)
@directive(name)
@directive(registry)
def adapter(scanner, pyname, ob, source, target, name, registry):
    pass
