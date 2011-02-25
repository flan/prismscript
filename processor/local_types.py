"""
types
=====
Purpose
-------
Provides core type-definitions for Prismscript.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: Feb. 20, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import random

class _Container:
    """
    A generic data-type for any structure that has a variable length.
    """
    def copy(self, **kwargs):
        return self.__class__(self)
        
    def contains(self, item, **kwargs):
        return item in self
        
    def _get_size(self):
        return len(self)
    length = property(_get_size)
    
class Dictionary(dict, _Container):
    """
    A Prismscript-friendly wrapper around a dictionary.
    
    Objects of this type may be passed to any Python function that expects a dict.
    """
    def __init__(self, items=[], **kwargs):
        dict.__init__(self, items)
        
    def get(self, key, default=None, **kwargs):
        return dict.get(self, key, default)
        
    def put(self, key, value, **kwargs):
        self[key] = value
        
    def remove(self, key, **kwargs):
        if key in self:
            del self[key]
            
    def get_items(self, **kwargs):
        items = Sequence()
        for item in self.items():
            items.append(Sequence(item))
        return items
        
    def get_keys(self, **kwargs):
        return Sequence(self.keys())
        
    def get_values(self, **kwargs):
        return Sequence(self.values())
        
class Set(set, _Container):
    """
    A Prismscript-friendly wrapper around a set.
    
    Objects of this type may be passed to any Python function that expects a set.
    """
    def __init__(self, items=[], **kwargs):
        set.__init__(self, items)
        
    def add(self, item, **kwargs):
        set.add(self, item)
        
    def remove(self, item, **kwargs):
        set.discard(self, item)
        
    def get_items(self, **kwargs):
        return Sequence(self)
        
    def difference(self, other_set, **kwargs):
        return Set(set.difference(self, other_set))
        
    def intersection(self, other_set, **kwargs):
        return Set(set.intersection(self, other_set))
        
    def union(self, other_set, **kwargs):
        return Set(set.union(self, other_set))
        
class Sequence(list, _Container):
    """
    A Prismscript-friendly wrapper around a list.
    
    Objects of this type may be passed to any Python function that expects a sequence.
    """
    def __init__(self, items=[], **kwargs):
        list.__init__(self, items)
        
    def append(self, item, **kwargs):
        list.append(self, item, **kwargs)
        
    def prepend(self, item, **kwargs):
        self.insert(0, item)
        
    def get(self, index, **kwargs):
        return self[index]
        
    def insert(self, index, item, **kwargs):
        list.insert(self, index, item)
        
    def remove(self, index, **kwargs):
        del self[index]
        
    def pop_head(self, **kwargs):
        return self.pop(0)
        
    def pop_item(self, index, **kwargs):
        return self.pop(index)
        
    def pop_tail(self, **kwargs):
        return self.pop()
        
    def reverse(self, **kwargs):
        list.reverse(self)
        
    def shuffle(self, **kwargs):
        random.shuffle(self)
        
    def sort(self, **kwargs):
        list.sort(self)
        
    def slice(self, start=None, end=None, **kwargs):
        if not start is None and not end is None:
            return self[start:end]
        elif not start is None:
            return self[start:]
        elif not end is None:
            return self[:end]
        else:
            return self.copy()
            