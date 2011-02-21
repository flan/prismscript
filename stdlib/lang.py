"""
stdlib.lang
===========
Purpose
-------
Provides core language features for Prismscript.

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
def build_range(stop, start=0, step=1, **kwargs):
    """
    Provides an iterator from `start` to `stop`, in increments of `range`, intended primarily for
    use in forloops that need to run a fixed number of times.
    """
    return range(start, stop, step)
    
