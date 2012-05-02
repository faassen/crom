from grokker import grokker, directive
from .directives import sources, target, name, registry
from . import current

@grokker
@directive(sources)
@directive(target)
@directive(name)
@directive(registry)
def component(scanner, pyname, obj, sources, target, name='', registry=None):
    if registry is None:
        def registry():
            return current.get_current()
    def register():
        registry().register(sources, target, name, obj)
    scanner.config.action(
        discriminator=('component', sources, target, name, registry),
        callable=register
        )

adapter = component
