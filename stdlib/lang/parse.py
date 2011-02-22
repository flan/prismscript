"""
stdlib.lang.parse
=================
Purpose
-------
Provides core parsing features for Prismscript.

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
def int(val, **kwargs):
    try:
        return __builtins__.int(val)
    except Exception:
        return 0
        
def str(val, **kwargs):
    return __builtins__.str(val)
    
def float(val, **kwargs):
    try:
        return __builtins__.float(val)
    except Exception:
        return 0.0
        
