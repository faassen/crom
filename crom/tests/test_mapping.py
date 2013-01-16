import py.test
from crom import MapKey, Map, MultiMap

def test_mapkey_without_parents():
    a = MapKey('a')
    assert a.key == 'a'
    assert a.parents == ()

def test_mapkey_with_parents():
    a = MapKey('a')
    b = MapKey('b', [a])
    assert b.parents == (a,)
    c = MapKey('c', (a,))
    assert c.parents == (a,)
    d = MapKey('d', [b, c])
    assert d.parents == (b, c)
    
def test_map_simple_key():
    m = Map()
    a = MapKey('a')
    m[a] = u'Value for A'
    assert m[a] == u'Value for A'

def test_map_same_underlying_key_is_same():
    m = Map()
    a = MapKey('a')
    a_another = MapKey('a')
    m[a] = u'Value for A'
    assert m[a_another] == u'Value for A'
    
def test_map_deletion():
    m = Map()
    a = MapKey('a')
    m[a] = u'Value for A'
    del m[a]
    with py.test.raises(KeyError):
        m[a]

def test_map_parent():
    m = Map()
    a = MapKey('a')
    b = MapKey('b', parents=[a])
    c = MapKey('c', parents=[a])
    m[b] = u'Value for B'
    assert m[b] == u'Value for B'
    with py.test.raises(KeyError):
        m[c]
    with py.test.raises(KeyError):
        m[a]

def test_map_ancestor():
    m = Map()
    
    a = MapKey('a')
    b = MapKey('b', parents=[a])

    m = Map()
    m[a] = u'Value for A'
    assert m[b] == u'Value for A'

def test_map_ancestor_mro():
    m = Map()
    a = MapKey('a')
    b = MapKey('b', parents=[a])
    c = MapKey('c', parents=[a])
    d = MapKey('d', parents=[b, c])
    
    m[b] = u'Value for B'
    m[c] = u'Value for C'

    # b comes first in mro
    assert m[d] == u'Value for B'

def test_map_ancestor_mro2():
    m = Map()
    a = MapKey('a')
    b = MapKey('b', parents=[a])
    c = MapKey('c', parents=[a])
    d = MapKey('d', parents=[b, c])
    
    m[c] = u'Value for C'

    # now we do get C
    assert m[d] == u'Value for C'
    
def test_map_ancestor_direct_key_wins():
    m = Map()
    a = MapKey('a')
    b = MapKey('b', parents=[a])
    c = MapKey('c', parents=[a])
    d = MapKey('d', parents=[b, c])
    
    m[b] = u'Value for B'
    m[c] = u'Value for C'
    m[d] = u'Value for D'
    
    assert m[d] == u'Value for D'

def test_map_all():
    m = Map()
    a = MapKey('a')
    b = MapKey('b', parents=[a])
    c = MapKey('c', parents=[a])
    d = MapKey('d', parents=[b, c])

    m[b] = u'Value for B'
    m[c] = u'Value for C'
    m[d] = u'Value for D'
    assert m.all(d) == [u'Value for D', u'Value for B', u'Value for C']

def test_map_all_empty(): 
    m = Map()
    a = MapKey('a')
    b = MapKey('b', parents=[a])
    c = MapKey('c', parents=[a])
    d = MapKey('d', parents=[b, c])

    m[b] = u'Value for B'
    m[c] = u'Value for C'
    m[d] = u'Value for D'
    assert m.all(d) == [u'Value for D', u'Value for B', u'Value for C']
   
def test_exact_getitem():
    m = Map()
    a = MapKey('a')
    b = MapKey('b', parents=[a])
    
    m[a] = u"Value for A"

    with py.test.raises(KeyError):
        m.exact_getitem(b)
    assert m.exact_getitem(a) == u'Value for A'

def test_exact_get():
    m = Map()
    a = MapKey('a')
    b = MapKey('b', parents=[a])
    
    m[a] = u"Value for A"

    assert m.exact_get(b) is None
    assert m.exact_get(b, u'default') == u'default'
    assert m.exact_get(a) == u'Value for A'
    
def test_multimap():
    m = MultiMap()

    alpha = MapKey('alpha')
    beta = MapKey('beta', [alpha])
    gamma = MapKey('gamma', [beta])

    one = MapKey('one')
    two = MapKey('two', [one])
    three = MapKey('three', [two])

    m[(alpha, three)] = u'Value for alpha, three'
    m[(beta, two)] = u'Value for beta, two'

    assert m[(alpha, three)] == u'Value for alpha, three'
    assert m[(beta, two)] == u'Value for beta, two'

    assert m[(gamma, two)] == u'Value for beta, two'
    assert m[(beta, three)] == u'Value for beta, two'
    assert m[(gamma, three)] == u'Value for beta, two'
    
    with py.test.raises(KeyError):
        m[(alpha, one)]
    with py.test.raises(KeyError):
        m[(alpha, two)]
    with py.test.raises(KeyError):
        m[(beta, one)]
        
def test_multimap_with_fallback():
    m = MultiMap()

    alpha = MapKey('alpha')
    beta = MapKey('beta', [alpha])
    gamma = MapKey('gamma', [beta])

    one = MapKey('one')
    two = MapKey('two', [one])
    three = MapKey('three', [two])

    m[(alpha, three)] = u'Value for alpha, three'
    m[(beta, two)] = u'Value for beta, two'

    # fallback
    m[(alpha, one)] = u'Value for alpha, one'

    # this gets the more specific interface
    assert m[(alpha, three)] == u'Value for alpha, three'
    assert m[(beta, two)] == u'Value for beta, two'

    assert m[(gamma, two)] == u'Value for beta, two'
    assert m[(beta, three)] == u'Value for beta, two'
    assert m[(gamma, three)] == u'Value for beta, two'

    # this uses the fallback
    assert m[(alpha, one)] == u'Value for alpha, one'
    assert m[(alpha, two)] == u'Value for alpha, one'
    assert m[(beta, one)] == u'Value for alpha, one'

@py.test.skip()
def test_multimap_all():
    m = MultiMap()

    alpha = MapKey('alpha')
    beta = MapKey('beta', [alpha])
    gamma = MapKey('gamma', [beta])

    one = MapKey('one')
    two = MapKey('two', [one])
    three = MapKey('three', [two])

    m[(alpha, three)] = u'Value for alpha, three'
    m[(beta, two)] = u'Value for beta, two'
    m[(alpha, one)] = u'Value for alpha, one'


    # this gets the more specific interface
    assert m.all((alpha, three)) == [u'Value for alpha, three',
                                     u'Value for alpha, one']
    assert m.all((beta, two)) == [u'Value for beta, two',
                                  u'Value for alpha, one']
    assert m.all((gamma, two)) == [u'Value for beta, two',
                                   u'Value for alpha, one']
    assert m.all((beta, three)) == [u'Value for beta, two',
                                    u'Value for alpha, one']
    assert m.all((gamma, three)) == [u'Value for beta, two',
                                     u'Value for alpha, one']

    # this uses the fallback only
    assert m.all((alpha, one)) == [u'Value for alpha, one']
    assert m.all((alpha, two)) == [u'Value for alpha, one']
    assert m.all((beta, one)) == [u'Value for alpha, one']


# XXX test_multimap_deletion
