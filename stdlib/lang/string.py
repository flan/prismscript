"""
stdlib.lang.string
==================
Purpose
-------
Provides string-manipulation features for Prismscript.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: Feb. 24, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import re
__no_recurse = (
 re,
)

def strip(s, **kwargs):
    return s.strip()
trim = strip

def lstrip(s, **kwargs):
    return s.lstrip()
ltrim = lstrip

def rstrip(s, **kwargs):
    return s.rstrip()
rtrim = rstrip

def contains(s, substring, **kwargs):
    return substring in s
    
def count(s, substring, **kwargs):
    return s.count(substring)
    
def replace(s, old, new, limit=0, **kwargs):
    if not limit:
        return s.replace(old, new)
    else:
        return s.replace(old, new, count)
        
def split(s, delimiter=' ', limit=0, from_left=True, **kwargs):
    split_function = s.split
    if not from_left:
        split_function = s.rsplit
        
    if limit:
        return split_function(delimiter, limit)
    return split_function(delimiter)
    
def ends_with(s, end, **kwargs):
    return s.endswith(end)
    
def starts_with(s, start, **kwargs):
    return s.startswith(start)
    
def filter(s, unwanted, **kwargs):
    return ''.join((c for c in s if not c in unwanted))
    
def filter_except(s, wanted, **kwargs):
    return ''.join((c for c in s if c in wanted))
    
def filter_unprintable(s, **kwargs):
    return ''.join((c for c in s if c.isprintable()))
    
def lower(s, **kwargs):
    return s.lower()
    
def upper(s, **kwargs):
    return s.upper()
    
def is_alpha(s, **kwargs):
    return s.isalpha()
    
def is_alphanumeric(s, **kwargs):
    return s.isalnum

def is_digit(s, **kwargs):
    return s.isdigit()
    
def is_number(s, **kwargs):
    return bool(re.match('^[-]?\d+(?:\.\d+)?$', s))
    
