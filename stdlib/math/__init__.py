"""
stdlib.lang.math.random
=======================
Purpose
-------
Provides math features for Prismscript.

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
import math as _math

from . import random
from . import trig

_abs = abs
_round = round

def get_e(**kwargs):
    return _math.e
    
def get_pi(**kwargs):
    return _math.pi
    
def abs(v, **kwargs):
    if type(v) == int:
        return _abs(v)
    return _math.fabs(v)
    
def ceil(v, **kwargs):
    return int(_math.ceil(v))
ceiling = ceil

def floor(v, **kwargs):
    return int(_math.floor(v))
    
def round(v, digits, **kwargs):
    return float(_round(v, digits))
    
def max(s, **kwargs):
    return max(s)
    
def min(s, **kwargs):
    return min(s)
    
def mean(items, **kwargs):
    total = sum(items)
    return total / len(items)
    
def median(items, **kwargs):
    if len(items) % 2: #Odd
        return items[floor(len(items) / 2)]
    else:
        target = len(items) / 2
        items = tuple(sorted(items))
        return (items[target - 1] + items[target]) / 2
        
def mode(items, **kwargs):
    buckets = {}
    for item in items:
        if item in buckets:
            buckets[item] += 1
        else:
            buckets[item] = 1
    (c, b) = max(((c, b) for (b, c) in buckets.items()))
    return b
    
def pow(v, exponent, **kwargs):
    return _math.pow(v, exponent)
    
def sqrt(v, **kwargs):
    return _math.sqrt(v)
    
def factorial(v, **kwargs):
    return _math.factorial(v)
    
def log(v, base, **kwargs):
    if base == 10:
        return _math.log10(v)
    return _math.log(v, base)
    
