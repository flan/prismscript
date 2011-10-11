"""
stdlib.lang.math.bitwise
========================
Purpose
-------
Provides random number features for Prismscript.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: Mar. 07, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
def b_and(x, y, **kwargs):
    return x & y
    
def b_or(x, y, **kwargs):
    return x | y
    
def b_xor(x, y, **kwargs):
    return x ^ y
    
def b_not(x, **kwargs):
    return ~x
    
def lshift(x, y, **kwargs):
    return x << y
    
def rshift(x, y, **kwargs):
    return x >> y
    
