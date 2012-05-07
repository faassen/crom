from crom import implicit
import threading

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
    
