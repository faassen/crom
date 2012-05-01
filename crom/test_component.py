from .component import InstanceRegistry
from crom import Interface, implements

class IAlpha(Interface):
    pass

@implements(IAlpha)
class Alpha(object):
    pass

class IBeta(Interface):
    pass

@implements(IBeta)
class Beta(object):
    pass

class ITarget(Interface):
    pass

def test_instance_no_source():
    reg = InstanceRegistry()
    foo = object()
    reg.register((), ITarget, '', foo)
    assert reg.lookup([], ITarget, '') is foo
    
def test_instance_one_source():
    reg = InstanceRegistry()
    foo = object()
    reg.register((IAlpha,), ITarget, '', foo)

    alpha = Alpha()
    assert reg.lookup([alpha], ITarget, '') is foo
    
def test_instance_two_sources():
    reg = InstanceRegistry()
    foo = object()
    reg.register((IAlpha, IBeta), ITarget, '', foo)

    alpha = Alpha()
    beta = Beta()
    assert reg.lookup([alpha, beta], ITarget, '') is foo

