import crom
from crom import testing

def setup_function(method):
    testing.setup()
    
def teardown_function(method):
    testing.teardown()

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

def test_new_grokker():
    from .fixtures import new_grokker as module
    # this module defines a new 'view' grokker that uses the
    # same registration machinery as the component grokker

    # grok the new grokker module
    crom.configure(module)
    # we should now be able to adapt things
    source = module.Source()
    view = module.ITarget(source, name='foo')
    assert module.ITarget.providedBy(view)
    assert isinstance(view, module.View)
    assert view.context is source
  
    
# XXX check the situation where a registry is passed
# that is an IRegistry instance. Will it conflict with
# the same registration on that registry correctly?
