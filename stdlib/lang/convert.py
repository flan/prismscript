"""
stdlib.lang.convert
===================
Purpose
-------
Provides core primitive-conversion features for Prismscript.

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
_int = int
_float = float

def float(v, **kwargs):
    try:
        return _float(v)
    except Exception:
        return 0.0
        
def int(v, **kwargs):
    try:
        return _int(v)
    except Exception:
        return 0
        
def string(v, **kwargs):
    return str(v)
    
