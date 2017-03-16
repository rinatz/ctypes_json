# -*- coding: utf-8 -*-


from ctypes import Array, Structure, Union
from json import JSONEncoder


class CDataJSONEncoder(JSONEncoder):
    def default(self, obj):
        return self._traverse(obj)

    def _traverse(self, obj):
        if isinstance(obj, Structure):
            return self._traverse_structure(obj)
        elif isinstance(obj, Union):
            return self._traverse_union(obj)
        elif isinstance(obj, Array):
            return [self._traverse(e) for e in obj]
        else:
            return obj

    def _traverse_structure(self, obj):
        result = {}
        anonymous = getattr(obj, '_anonymous_', [])

        for fields in getattr(obj, '_fields_', []):
            key = fields[0]
            value = getattr(obj, key)

            if key.startswith('_'):
                continue

            if key in anonymous:
                result.update(self._traverse(value))
            else:
                result[key] = self._traverse(value)

        return result

    _traverse_union = _traverse_structure


class DictMixIn(object):
    def __getitem__(self, item):
        return getattr(self, item)

    def __contains__(self, item):
        try:
            _ = getattr(self, item)
        except AttributeError:
            return False

        return True

    def __iter__(self):
        return self.keys()

    @property
    def dict(self):
        return CDataJSONEncoder().default(self)

    def keys(self):
        for field in getattr(self, '_fields_', []):
            yield field[0]

    def values(self):
        for field in getattr(self, '_fields_', []):
            yield getattr(self, field[0])

    def items(self):
        for field in getattr(self, '_fields_', []):
            key = field[0]
            value = getattr(self, key)

            yield key, value


class DictStructure(Structure, DictMixIn): pass
class DictUnion(Union, DictMixIn): pass
