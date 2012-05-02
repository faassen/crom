from grokker import grokker, directive
from .directives import sources, target, name, registry
from .current import get_registry
from .interfaces import IRegistry

@grokker
@directive(sources)
@directive(target)
@directive(name)
@directive(registry)
def component(scanner, pyname, obj, sources, target, name='',
              registry=get_registry):
    def register():
        found_registry = registry
        if not IRegistry.providedBy(found_registry):
            found_registry = registry()
        found_registry.register(sources, target, name, obj)
    scanner.config.action(
        discriminator=('component', sources, target, name, registry),
        callable=register
        )

adapter = component
