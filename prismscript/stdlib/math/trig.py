"""
stdlib.lang.math.trig
=====================
Purpose
-------
Provides trigonometric features for Prismscript.

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
import math
__no_recurse = (
 math,
)

def degrees(x, **kwargs):
    return math.degrees(x)
    
def radians(x, **kwargs):
    return math.radians(x)
    
def hypotenuse(x, y, **kwargs):
    return math.hypot(x, y)
    
def acos(x, **kwargs):
    return math.acos(x)
    
def asin(x, **kwargs):
    return math.asin(x)
    
def atan(x, y=None, **kwargs):
    if not y is None:
        return math.atan2(x, y)
    return math.atan(x)
    
def cos(x, **kwargs):
    return math.cos(x)
    
def sin(x, **kwargs):
    return math.sin(x)
    
def tan(x, **kwargs):
    return math.tan(x)
    
def acosh(x, **kwargs):
    return math.acosh(x)
    
def asinh(x, **kwargs):
    return math.asinh(x)
    
def atanh(x, **kwargs):
    return math.atanh(x)
    
def cosh(x, **kwargs):
    return math.cosh(x)
    
def sinh(x, **kwargs):
    return math.sinh(x)
    
def tanh(x, **kwargs):
    return math.tanh(x)
    
