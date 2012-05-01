import py.test
from .registry import Registry
from crom import Interface, implements, ComponentLookupError

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

def test_component_no_source():
    reg = Registry()
    foo = object()
    reg.register((), ITarget, '', foo)
    assert reg.lookup([], ITarget, '') is foo
    assert ITarget.utility(registry=reg) is foo
    
def test_component_one_source():
    reg = Registry()
    foo = object()
    reg.register((IAlpha,), ITarget, '', foo)

    alpha = Alpha()
    assert reg.lookup([alpha], ITarget, '') is foo
    assert ITarget.utility(alpha, registry=reg) is foo
    
def test_component_two_sources():
    reg = Registry()
    foo = object()
    reg.register((IAlpha, IBeta), ITarget, '', foo)

    alpha = Alpha()
    beta = Beta()
    assert reg.lookup([alpha, beta], ITarget, '') is foo
    assert ITarget.utility(alpha, beta, registry=reg) is foo
    
def test_component_class_based_registration():
    reg = Registry()
    foo = object()
    reg.register((Alpha,), ITarget, '', foo)

    alpha = Alpha()
    assert reg.lookup([alpha], ITarget, '') is foo
    assert ITarget.utility(alpha, registry=reg) is foo
    
def test_component_inheritance():
    reg = Registry()
    foo = object()

    class Gamma(object):
        pass

    class Delta(Gamma):
        pass
    
    reg.register([Gamma], ITarget, '', foo)

    delta = Delta()
    
    assert reg.lookup([delta], ITarget, '') is foo
    assert ITarget.utility(delta, registry=reg) is foo
    
def test_component_not_found():
    reg = Registry()
    
    assert reg.lookup([], ITarget, '') is None
    alpha = Alpha()
    assert reg.lookup([alpha], ITarget, '') is None
    assert ITarget.utility(alpha, registry=reg, default=None) is None
    with py.test.raises(ComponentLookupError):
        ITarget.utility(alpha, registry=reg)

def test_component_to_itself():
    reg = Registry()
    alpha = Alpha()

    foo = object()
    
    reg.register([IAlpha], IAlpha, '', foo)

    assert reg.lookup([alpha], IAlpha, '') is foo
    assert IAlpha.utility(alpha, registry=reg) is foo
    
def test_adapter_no_source():
    reg = Registry()

    foo = object()
    def factory():
        return foo
    
    reg.register((), ITarget, '', factory)

    assert reg.get_adapter([], ITarget, '') is foo
    assert ITarget.adapter(registry=reg) is foo
    assert ITarget(registry=reg) is foo
    
def test_adapter_one_source():
    reg = Registry()

    @implements(ITarget)
    class Adapted(object):
        def __init__(self, context):
            self.context = context
    
    reg.register([IAlpha], ITarget, '', Adapted)
    
    alpha = Alpha()
    adapted = reg.get_adapter([alpha], ITarget, '')
    assert isinstance(adapted, Adapted)
    assert adapted.context is alpha
    adapted = ITarget(alpha, registry=reg)
    assert isinstance(adapted, Adapted)
    assert adapted.context is alpha
    adapted = ITarget.adapter(alpha, registry=reg)
    assert isinstance(adapted, Adapted)
    assert adapted.context is alpha
    
def test_adapter_to_itself():
    reg = Registry()

    alpha = Alpha()

    @implements(IAlpha)
    class Adapter(object):
        def __init__(self, context):
            self.context = context

    # behavior without any registration; we get the object back
    assert reg.get_adapter([alpha], IAlpha, '') is alpha
    assert IAlpha(alpha, registry=reg) is alpha
    # it works even without registry
    assert IAlpha(alpha) is alpha
    
    # behavior is the same with registration
    reg.register([IAlpha], IAlpha, '', Adapter)
    assert reg.get_adapter([alpha], IAlpha, '') is alpha
    assert IAlpha(alpha, registry=reg) is alpha
    assert IAlpha(alpha) is alpha
    
def test_adapter_two_sources():
    reg = Registry()

    @implements(ITarget)
    class Adapted(object):
        def __init__(self, alpha, beta):
            self.alpha = alpha
            self.beta = beta

    reg.register([IAlpha, IBeta], ITarget, '', Adapted)

    alpha = Alpha()
    beta = Beta()
    adapted = reg.get_adapter([alpha, beta], ITarget, '')

    assert isinstance(adapted, Adapted)
    assert adapted.alpha is alpha
    assert adapted.beta is beta

    adapted = ITarget(alpha, beta, registry=reg)
    assert isinstance(adapted, Adapted)
    assert adapted.alpha is alpha
    assert adapted.beta is beta

    adapted = ITarget.adapter(alpha, beta, registry=reg)
    assert isinstance(adapted, Adapted)
    assert adapted.alpha is alpha
    assert adapted.beta is beta
    
