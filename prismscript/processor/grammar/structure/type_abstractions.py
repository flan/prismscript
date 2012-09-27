"""
structure.type_abstractions
===========================
Purpose
-------
Provides portable definitions for the "primitive" types in Prismscript.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Sept. 27, 2012

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
try:
    unicode
except NameError: #unicode was merged with string in py3k
    unicode = str

class String(unicode):
    def new_method(self):
        #use self directly
