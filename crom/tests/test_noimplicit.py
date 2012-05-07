import threading
from zope.configuration.config import ConfigurationExecutionError
import py.test

from crom import implicit, monkey
import crom
from crom.interfaces import NoImplicitRegistryError, NoImplicitLookupError

def setup_function(f):
    monkey.incompat()

def teardown_function(f):
    monkey.revert_incompat()
    
def test_no_implicit_initialization():

    assert implicit.registry is None
    assert implicit.lookup is None
    assert implicit.base_lookup is None
    
    log = []
    def f():
        log.append(implicit.registry)
        log.append(implicit.lookup)
        log.append(implicit.base_lookup)
    
    thread = threading.Thread(target=f)
    thread.start()
    thread.join()

    assert log[0] is None
    assert log[1] is None
    assert log[2] is None
    
def test_no_implicit_grokking():
    from .fixtures import component as module
    # grok the component module
    with py.test.raises(ConfigurationExecutionError) as e:
        crom.configure(module)
    assert isinstance(e.value.evalue, NoImplicitRegistryError)

def test_no_implicit_lookup():
    from .fixtures import component as module
    # don't grok this, but that's not important, we just want the
    # stuff in module to test

    source = module.Source()

    # we try to adapt without an explicit lookup, this will fail
    with py.test.raises(NoImplicitLookupError):
        adapted = module.ITarget(source)
