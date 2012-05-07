from grokker import grokker, directive, Directive
from .directives import sources, target, name
from .implicit import implicit
from .interfaces import IRegistry, NoImplicitRegistryError

def registry_converter(registry):
    if registry is not None:
        if not IRegistry.providedBy(registry):
            return registry()
        return registry
    if implicit.registry is None:
        raise NoImplicitRegistryError(
            "Cannot register without explicit "
            "registry decorator because implicit registry "
            "is not configured.")
    return implicit.registry

# this needs to be defined here to avoid circular imports
registry = Directive('registry', 'crom', converter=registry_converter)

@grokker
@directive(sources)
@directive(target)
@directive(name)
@directive(registry)
def component(scanner, pyname, obj, sources, target, registry, name=''):
    def register():
        registry.register(sources, target, name, obj)
    scanner.config.action(
        discriminator=('component', sources, target, name, registry),
        callable=register
        )

adapter = component
