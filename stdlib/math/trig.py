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
import math as _math

def degrees(x, **kwargs):
    return _math.degrees(x)
    
def radians(x, **kwargs):
    return _math.radians(x)
    
def hypotenuse(x, y, **kwargs):
    return _math.hypot(x, y)
    
def acos(x, **kwargs):
    return _math.acos(x)
    
def asin(x, **kwargs):
    return _math.asin(x)
    
def atan(x, y=None, **kwargs):
    if not y is None:
        return _math.atan2(x, y)
    return _math.atan(x)
    
def cos(x, **kwargs):
    return _math.cos(x)
    
def sin(x, **kwargs):
    return _math.sin(x)
    
def tan(x, **kwargs):
    return _math.tan(x)
    
def acosh(x, **kwargs):
    return _math.acosh(x)
    
def asinh(x, **kwargs):
    return _math.asinh(x)
    
def atanh(x, **kwargs):
    return _math.atanh(x)
    
def cosh(x, **kwargs):
    return _math.cosh(x)
    
def sinh(x, **kwargs):
    return _math.sinh(x)
    
def tanh(x, **kwargs):
    return _math.tanh(x)
    
