import crom

class ISource(crom.Interface):
    pass

class ITarget(crom.Interface):
    pass

@crom.implements(ISource)
class Source(object):
    pass

@crom.adapter
@crom.sources(ISource)
@crom.target(ITarget)
@crom.implements(ITarget)
class Adapter(object):
    def __init__(self, context):
        self.context = context
