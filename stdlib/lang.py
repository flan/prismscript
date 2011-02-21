"""
stdlib.lang
===========
Purpose
-------
Provides core language features for Prismscript.

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
class _Keystore(dict):
    """
    A Prismscript-friendly wrapper around a dictionary.
    
    Supported-but-undefined functions:
        .copy()
        .items()
        .keys()
        .values()
    """
    def contains(self, key, **kwargs):
        return key in self
        
    def get(self, key, default=None, **kwargs):
        return dict.get(self, key, default)
        
    def put(self, key, value, **kwargs):
        self[key] = value
        
    def remove(self, key, **kwargs):
        if key in self:
            del self[key]
            
class _Set(set):
    """
    A Prismscript-friendly wrapper around a set.
    
    Supported-but-undefined functions:
        .copy()
    """
    def add(self, item, **kwargs):
        set.add(self, item)
        
    def remove(self, item, **kwargs):
        set.discard(self, item)
        
    def difference(self, other_set, **kwargs):
        return _Set(set.difference(self, other_set))
        
    def intersection(self, other_set, **kwargs):
        return _Set(set.intersection(self, other_set))
        
    def is_subset(self, other_set, **kwargs):
        return set.issubset(self, other_set)
        
    def is_superset(self, other_set, **kwargs):
        return _Set(set.issuperset(self, other_set))
        
    def to_sequence(self, **kwargs):
        return list(self)
        
    def union(self, other_set, **kwargs):
        return _Set(set.union(self, other_set))
        
def build_range(stop, start=0, step=1, **kwargs):
    """
    Provides an iterator from `start` to `stop`, in increments of `range`, intended primarily for
    use in forloops that need to run a fixed number of times.
    """
    return range(start, stop, step)
    
def Keystore(items=[], **kwargs):
    """
    Returns a new key-value store (dictionary), pre-populated with `items`, a Sequence of
    (key, value) tuples.
    """
    return _Keystore(items)
    
def Set(items=[], **kwargs):
    """
    Returns a new set, pre-populated with `items`, a Sequence.
    """
    return _Set(items)
    
