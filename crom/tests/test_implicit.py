import threading
from crom.implicit import implicit

def test_lookup_in_main():
    implicit.initialize()

    assert implicit.lookup is implicit.registry
    
def test_lookup_in_thread_uses_default():
    implicit.initialize()
    
    log = []
    def f():
        log.append(implicit.lookup)
    
    thread = threading.Thread(target=f)
    thread.start()
    thread.join()
    assert len(log) == 1
    assert log[0] is implicit.registry

def test_changed_lookup_in_thread_doesnt_affect_main():
    implicit.initialize()

    # a different ILookup
    # (we don't actually fulfill the interface as that's not needed for
    # this test)
    different_lookup = object()

    log = []
    def f():
        implicit.lookup = different_lookup
        log.append(implicit.lookup)
    
    thread = threading.Thread(target=f)
    thread.start()
    thread.join()
    assert len(log) == 1
    assert log[0] is different_lookup
    assert implicit.lookup is implicit.registry
    assert implicit.lookup is implicit.base_lookup
