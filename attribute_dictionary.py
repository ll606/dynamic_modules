from collections.abc import Mapping


class ReadOnlyAttributeDictionary:
    
    def __init__(self, values: dict) -> None:
        self._data = values
    
    def __getattr__(self, name: str):
        data = object.__getattribute__(self, '_data')
        try:
            return data[name]
        except KeyError:
            raise AttributeError(
                'AttributeDictionary does not'
                ' have the key of %s' % name
            ) from None
    
    __getitem__ = __getattr__
    
    
    def keys(self):
        return object.__getattribute__(self, '_data').keys()
    
    def values(self):
        return object.__getattribute__(self, '_data').values()
    
    def items(self):
        return object.__getattribute__(self, '_data').items()
    
    def get(self, key, default=None):
        data = object.__getattribute__(self, '_data')
        return data.get(key, default)
    
    def __iter__(self):
        return object.__getattribute__(self, '_data').__iter__()
    
    def __contains__(self, other):
        return object.__getattribute__(self, '_data').__contains__(other)
    
    def __copy__(self):
        data = object.__getattribute__(self, '_data').copy()
        return __class__(data)
    
    def __len__(self):
        return len(object.__getattribute__(self, '_data'))
    
class AttributeDictionary(ReadOnlyAttributeDictionary):
    
    def __init__(self, values: dict=None) -> None:
        if values is None:
            values = {}
        object.__setattr__(self, '_data', values)
    
    def __setitem__(self, key, value):
        data = object.__getattribute__(self, '_data')
        data[key] = value
    
    __setattr__ = __setitem__
    
    def __delitem__(self, key):
        data = object.__getattribute__(self, '_data')
        del data[key]
    
    __delattr__ = __delitem__
    
    
    def update(self, other):
        return object.__getattribute__(self, '_data').update(other)
    
    def pop(self, key):
        return object.__getattribute__(self, '_data').pop(key)
    
    def popitem(self):
        return object.__getattribute__(self, '_data').popitem()
    
    def clear(self):
        return object.__getattribute__(self, '_data').clear()
    
    def __eq__(self, other):
        if isinstance(other, ReadOnlyAttributeDictionary):
            other = other._data
        return object.__getattribute__(self, '_data').__eq__(other)