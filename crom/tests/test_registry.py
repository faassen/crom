import py.test
from crom.registry import Registry
from crom import Interface, implements, ComponentLookupError
from crom import monkey

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

def setup_function(method):
    monkey.incompat()

def teardown_function(method):
    monkey.revert_incompat()
    
def test_component_no_source():
    reg = Registry()
    foo = object()
    reg.register((), ITarget, '', foo)
    assert reg.lookup([], ITarget, '') is foo
    assert ITarget.component(lookup=reg) is foo
    
def test_component_one_source():
    reg = Registry()
    foo = object()
    reg.register((IAlpha,), ITarget, '', foo)

    alpha = Alpha()
    assert reg.lookup([alpha], ITarget, '') is foo
    assert ITarget.component(alpha, lookup=reg) is foo
    
def test_component_two_sources():
    reg = Registry()
    foo = object()
    reg.register((IAlpha, IBeta), ITarget, '', foo)

    alpha = Alpha()
    beta = Beta()
    assert reg.lookup([alpha, beta], ITarget, '') is foo
    assert ITarget.component(alpha, beta, lookup=reg) is foo
    
def test_component_class_based_registration():
    reg = Registry()
    foo = object()
    reg.register((Alpha,), ITarget, '', foo)

    alpha = Alpha()
    assert reg.lookup([alpha], ITarget, '') is foo
    assert ITarget.component(alpha, lookup=reg) is foo
    
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
    assert ITarget.component(delta, lookup=reg) is foo
    
def test_component_not_found():
    reg = Registry()
    
    assert reg.lookup([], ITarget, '') is None
    alpha = Alpha()
    assert reg.lookup([alpha], ITarget, '') is None
    assert ITarget.component(alpha, lookup=reg, default=None) is None
    with py.test.raises(ComponentLookupError):
        ITarget.component(alpha, lookup=reg)

def test_component_to_itself():
    reg = Registry()
    alpha = Alpha()

    foo = object()
    
    reg.register([IAlpha], IAlpha, '', foo)

    assert reg.lookup([alpha], IAlpha, '') is foo
    assert IAlpha.component(alpha, lookup=reg) is foo
    
def test_adapter_no_source():
    reg = Registry()

    foo = object()
    def factory():
        return foo
    
    reg.register((), ITarget, '', factory)

    assert reg.adapt([], ITarget, '') is foo
    assert ITarget.adapt(lookup=reg) is foo
    assert ITarget(lookup=reg) is foo
    
def test_adapter_one_source():
    reg = Registry()

    @implements(ITarget)
    class Adapted(object):
        def __init__(self, context):
            self.context = context
    
    reg.register([IAlpha], ITarget, '', Adapted)
    
    alpha = Alpha()
    adapted = reg.adapt([alpha], ITarget, '')
    assert isinstance(adapted, Adapted)
    assert adapted.context is alpha
    adapted = ITarget(alpha, lookup=reg)
    assert isinstance(adapted, Adapted)
    assert adapted.context is alpha
    adapted = ITarget.adapt(alpha, lookup=reg)
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
    assert reg.adapt([alpha], IAlpha, '') is alpha
    assert IAlpha(alpha, lookup=reg) is alpha
    # it works even without registry
    assert IAlpha(alpha) is alpha
    
    # behavior is the same with registration
    reg.register([IAlpha], IAlpha, '', Adapter)
    assert reg.adapt([alpha], IAlpha, '') is alpha
    assert IAlpha(alpha, lookup=reg) is alpha
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
    adapted = reg.adapt([alpha, beta], ITarget, '')

    assert isinstance(adapted, Adapted)
    assert adapted.alpha is alpha
    assert adapted.beta is beta

    adapted = ITarget(alpha, beta, lookup=reg)
    assert isinstance(adapted, Adapted)
    assert adapted.alpha is alpha
    assert adapted.beta is beta

    adapted = ITarget.adapt(alpha, beta, lookup=reg)
    assert isinstance(adapted, Adapted)
    assert adapted.alpha is alpha
    assert adapted.beta is beta
    
def test_default():
    reg = Registry()

    assert ITarget.component(lookup=reg, default='blah') == 'blah'

def test_name():
    reg = Registry()
    foo = object()
    reg.register([Alpha], ITarget, 'x', foo)
    alpha = Alpha()
    assert ITarget.component(alpha, lookup=reg, name='x') is foo
    assert ITarget.component(alpha, lookup=reg, default=None) is None
    
def test_non_adapter_looked_up_as_adapter():
    reg = Registry()
    foo = object()
    reg.register([Alpha], ITarget, '', foo)
    alpha = Alpha()
    with py.test.raises(TypeError):
        ITarget(alpha, lookup=reg)
    
def test_adapter_with_wrong_args():
    class Adapter(object):
        # takes no args
        def __init__(self):
            pass
    reg = Registry()
    reg.register([Alpha], ITarget, '', Adapter)
    alpha = Alpha()
    
    with py.test.raises(TypeError) as e:
        ITarget(alpha, lookup=reg)

    assert str(e.value) == ("__init__() takes exactly 1 argument (2 given) "
                            "(<class 'crom.tests.test_registry.Adapter'>)")
    
def test_extra_kw():
    reg = Registry()
    foo = object()
    
    reg.register([Alpha], ITarget, '', foo)
    alpha = Alpha()
    
    with py.test.raises(TypeError) as e:
        ITarget.component(alpha, lookup=reg, extra="illegal")
    assert str(e.value) == 'Illegal extra keyword arguments: extra'
