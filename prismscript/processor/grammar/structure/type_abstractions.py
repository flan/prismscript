"""
structure.type_abstractions
===========================
Purpose
-------
Provides portable definitions for the "primitive" types in Prismscript.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Sept. 27, 2012

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import random
import re
import types
import warnings

try:
    unicode
except NameError: #unicode was merged with string in py3k
    unicode = str

def convert_bool(v, **kwargs):
    return bool(v)
    
def convert_float(v, **kwargs):
    try:
        return float(v)
    except Exception:
        return None
        
def convert_int(v, base=None, is_char=False, **kwargs):
    try:
        if base:
            return int(v, base)
        elif is_char:
            return ord(v)
        else:
            return int(v)
    except Exception:
        return None
        
def convert_string(v, int_base=None, is_char=False, **kwargs):
    if int_base:
        if not 2 <= int_base <= 36:
            raise ValueError("Integer base must be between 2 and 36, inclusive, not %(i)r" % {
             'i': int_base,
            })
        if not type(v) == int:
            raise ValueError("Unable to process non-integer value %(i)r" % {
             'i': v,
            })
        num_base = 48 #Ascii 0
        asc_offset = 39 #Distance from 0 to 'a'.
        output = []
        while v:
            v_mod = v % int_base
            v //= int_base
            output.insert(0, chr(num_base + v_mod + (v_mod > 10 and asc_offset or 0)))
        return String(''.join(output))
    elif is_char:
        return String(chr(v))
    else:
        return String(v)

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
    
    def join(self, s, **kwargs):
        return String(s.join((str(element) for element in self)))
        
class String(unicode, _Container):
    """
    A Prismscript-friendly wrapper around a string.
    """
    def trim(self, characters=None, **kwargs):
        return String(self.strip(characters and ''.join(characters)))
        
    def ltrim(self, characters=None, **kwargs):
        return String(self.lstrip(characters and ''.join(characters)))
        
    def rtrim(self, characters=None, **kwargs):
        return String(self.rstrip(characters and ''.join(characters)))
        
    def reverse(self, **kwargs):
        return String(''.join(reversed(self)))
        
    def count(self, item, start=None, end=None, **kwargs):
        return String(self.count(item, start, end))
        
    def replace(self, old, new, limit=-1, **kwargs):
        return String(self.replace(old, new, limit))
        
    def split(self, delimiter=' ', limit=-1, from_left=True, **kwargs):
        if from_left:
            result = unicode.split(self, delimiter, limit)
        else:
            result = self.rsplit(delimiter, limit)
        return Sequence((String(s) for s in result))
        
    def ends_with(self, end, **kwargs):
        return String(self.endswith(end))
        
    def starts_with(self, start, **kwargs):
        return String(self.startswith(start))
        
    def filter(self, unwanted, **kwargs):
        return String(''.join((c for c in self if not c in unwanted)))
        
    def filter_except(self, wanted, **kwargs):
        return String(''.join((c for c in self if c in wanted)))
        
    def filter_unprintable(self, **kwargs):
        return String(''.join((c for c in self if c.isprintable())))
        
    def lower(self, **kwargs):
        return String(self.lower())
        
    def upper(self, **kwargs):
        return String(self.upper())
        
    def is_alpha(self, **kwargs):
        return String(self.isalpha())
        
    def is_alphanumeric(self, **kwargs):
        return String(self.isalnum())

    def is_digit(self, **kwargs):
        return String(self.isdigit())
        
    def is_number(self, **kwargs):
        return String(bool(re.match('^[-]?\d+(?:\.\d+)?$', self)))
        
    def is_regex_match(self, r, **kwargs):
        return String(bool(re.match(r, self)))
        
    def format(self, values, **kwargs):
        return String(self % tuple(values))
        
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
