"""
stdlib.lang.math.random
=======================
Purpose
-------
Provides random number features for Prismscript.

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
import random as _random

def randint(high, low=0, **kwargs):
    return _random.randint(low, high)
    
def uniform(low=0.0, high=1.0, **kwargs):
    return _random.uniform(low, high)
    
def sample(items, sample_size, **kwargs):
    return _random.sample(items, sample_size)
    
def choose(items, **kwargs):
    return _random.choice(items)
    
