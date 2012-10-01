"""
stdlib.util.time
==================
Purpose
-------
Provides time-accounting features for Prismscript.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: Nov. 2, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import sys as _sys
_time = _sys.modules['time']
__no_recurse = (
 _time,
 _sys,
)

def asctime(t, **kwargs):
    return _time.ctime(t)

def utctime(**kwargs):
    return _time.time()

def sleep(t, **kwargs):
    _time.sleep(t)
    
