import crom
from crom import monkey

def setup_function(method):
    monkey.incompat()

def teardown_function(method):
    monkey.revert_incompat()

def test_component():
    from .fixtures import component as module
    # grok the component module
    crom.configure(module)
    # we should now be able to adapt things
    source = module.Source()
    adapted = module.ITarget(source)
    assert module.ITarget.providedBy(adapted)
    assert isinstance(adapted, module.Adapter)
    assert adapted.context is source

