from .component import InstanceRegistry, Registry
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

def test_instance_class_based_registration():
    reg = InstanceRegistry()
    foo = object()
    reg.register((Alpha,), ITarget, '', foo)

    alpha = Alpha()
    assert reg.lookup([alpha], ITarget, '') is foo

def test_instance_inheritance():
    reg = InstanceRegistry()
    foo = object()

    class Gamma(object):
        pass

    class Delta(Gamma):
        pass
    
    reg.register([Gamma], ITarget, '', foo)

    delta = Delta()
    
    assert reg.lookup([delta], ITarget, '') is foo

def test_instance_not_found():
    reg = InstanceRegistry()
    
    assert reg.lookup([], ITarget, '') is None
    alpha = Alpha()
    assert reg.lookup([alpha], ITarget, '') is None
    
def test_utility_no_source():
    reg = Registry()
    foo = object()
    reg.register_utility((), ITarget, '', foo)
    assert reg.get_utility([], ITarget, '') is foo

def test_utility_one_source():
    reg = Registry()
    foo = object()
    reg.register_utility([IAlpha], ITarget, '', foo)

    alpha = Alpha()
    assert reg.get_utility([alpha], ITarget, '') is foo

def test_utility_two_sources():
    reg = Registry()
    foo = object()
    reg.register_utility([IAlpha, IBeta], ITarget, '', foo)

    alpha = Alpha()
    beta = Beta()
    assert reg.get_utility([alpha, beta], ITarget, '') is foo
    
def test_adapter_no_source():
    reg = Registry()

    foo = object()
    def factory():
        return foo
    
    reg.register_adapter((), ITarget, '', factory)

    assert reg.get_adapter([], ITarget, '') is foo
    
def test_adapter_one_source():
    reg = Registry()

    @implements(ITarget)
    class Adapted(object):
        def __init__(self, context):
            self.context = context
    
    reg.register_adapter([IAlpha], ITarget, '', Adapted)
    
    alpha = Alpha()
    adapted = reg.get_adapter([alpha], ITarget, '')
    assert isinstance(adapted, Adapted)
    assert adapted.context is alpha
    
def test_adapter_two_sources():
    reg = Registry()

    @implements(ITarget)
    class Adapted(object):
        def __init__(self, alpha, beta):
            self.alpha = alpha
            self.beta = beta

    reg.register_adapter([IAlpha, IBeta], ITarget, '', Adapted)

    alpha = Alpha()
    beta = Beta()
    adapted = reg.get_adapter([alpha, beta], ITarget, '')

    assert isinstance(adapted, Adapted)
    assert adapted.alpha is alpha
    assert adapted.beta is beta
    

