class MapKey(object):
    """A map key that can have parents.
    """
    def __init__(self, key, parents=()):
        self.key = key
        self.parents = tuple(parents)
        # we need Python's mro, but we don't have classes. We create
        # some with the same structure as our parent structure. then we
        # get the mro
        self._mro_helper = type('fake_type',
                                tuple(parent._mro_helper for
                                      parent in parents),
                                {'mapkey': self})
        # we then store the map keys for the mro (without the last
        # entry, which is always object)
        self._parent_mapkeys = [
            base.mapkey for base in self._mro_helper.__mro__[:-1]]

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def __repr__(self):
        return "<MapKey: %r>" % self.key

class Map(dict):
    """special map that understands about keys in a dag.
    
    A normal mapping (dictionary) in Python has keys that are
    completely independent from each other. If you look up a
    particular key, either that key is present in the mapping or not
    at all.

    This is a mapping that understands about relations between
    keys. Keys can have zero or more parents; they are in a directed
    acyclic graph. If a key is not found, a value will still be found
    if a parent key can be found.
    """
    # sometimes we want to look up things exactly in the underlying
    # dictionary
    exact_getitem = dict.__getitem__
    exact_get = dict.get
    
    def __getitem__(self, key):
        for mapkey in key._parent_mapkeys:
            try:
                # XXX can this be an exact_getitem instead?
                return self.exact_getitem(mapkey)
            except KeyError:
                pass
        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def all(self, key):
        result = []
        for mapkey in key._parent_mapkeys:
            try:
                result.append(self.exact_getitem(mapkey))
            except KeyError:
                pass
        return result
    
class MultiMap(object):
    """map that takes sequences of MapKey objects as key.

    A MultiMap is a map that takes sequences of MapKey objects as its
    key. We call such a sequence of MapKeys a MultiMapKey.

    When looking up a MultiMapKey in a MultiMap, it is compared
    component-wise to the MultiMapKeys registered in the MultiMap.
    Each of the components of a MultiMapKey found must be either equal
    to or a parent of the corresponding component of the MultiMapKey
    being looked up.  If more than one MultiMapKey could be found by a
    lookup, the one whose first component matches most specifically
    wins, the other components being considered as subordinate
    comparison criteria, in order.
    """
    def __init__(self):
        self._by_arity = {}
        
    def __setitem__(self, key, value):
        arity = MapKey(len(key))
        key = [arity] + list(key)
        last_key = key.pop()
        map = self._by_arity
        for k in key:
            # XXX why is the dict() call here?
            submap = dict(map).get(k)
            if submap is None:
                submap = map[k] = Map()
            map = submap
        map[last_key] = value

    def __delitem__(self, key):
        arity = MapKey(len(key))
        key = [arity] + list(key)
        last_key = key.pop()
        map = self._by_arity
        for k in key:
            map = dict(map)[k]
        del map[last_key]

    def __getitem__(self, key):
        arity = MapKey(len(key))
        key = [arity] + list(key)
        return self._getitem_recursive(self._by_arity, key)

    # XXX missing exact_getitem, exact_get

    def _getitem_recursive(self, map, key):
        first = key[0]
        rest = key[1:]
        if not rest:
            return map[first]
        for parent in first._parent_mapkeys:
            try:
                return self._getitem_recursive(map[parent], rest)
            except KeyError, e:
                pass
        raise e

    def all(self, key):
        arity = MapKey(len(key))
        key = [arity] + list(key)
        found = {}
        return self._all_recursive(found, self._by_arity, key)

    def _all_recursive(self, found, map, key):
        value = found.get(key)
        if value is not None:
            return value
        first = key[0]
        rest = key[1:]
        if not rest:
            value = map.all(first)
            found[first] = value
            return value
        result = []
        for parent in first._parent_mapkeys:
            try:
                result.extend(self._all_recursive(found, map[parent], rest))
            except KeyError, e:
                pass
        found[key] = result
        return result

    
