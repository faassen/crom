import threading
#from crom.current import current

# def test_lookup_in_thread_uses_default():
#     foo = object()
#     current.registry = foo
#     current.lookup = current.registry
    
#     log = []
#     def f():
#         log.append(current.lookup)
    
#     thread = threading.Thread(target=f)
#     thread.start()
#     thread.join()
#     assert len(log) == 1
#     assert log[0] is foo

# def test_changed_lookup_in_thread_doesnt_affect_main():
#     foo = object()
#     bar = object()
#     current.registry = foo
#     current.lookup = current.registry
    
#     log = []
#     def f():
#         current.lookup = bar
#         log.append(current.lookup)
    
#     thread = threading.Thread(target=f)
#     thread.start()
#     thread.join()
#     assert len(log) == 1
#     assert log[0] is bar
#     assert current.lookup is foo
    
