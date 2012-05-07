import crom
import grokker

@grokker.grokker
@grokker.directive(crom.sources)
@grokker.directive(crom.name)
@grokker.directive(crom.registry)
def view(scanner, pyname, obj, sources, registry, name):
    def register():
        registry.register(sources, ITarget, name, obj)
    scanner.config.action(
        discriminator=('component', sources, ITarget, name, registry),
        callable=register
        )

class ISource(crom.Interface):
    pass

class ITarget(crom.Interface):
    pass

@crom.implements(ISource)
class Source(object):
    pass

@view
@crom.name('foo')
@crom.sources(ISource)
@crom.implements(ITarget)
class View(object):
    def __init__(self, context):
        self.context = context
