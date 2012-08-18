"""
tests (package)
===============
Purpose
-------
Provides test-oriented access to the language's interpreter, allowing for a high degree of
semantics-oriented introspection and analysis to support rapid diagnosis of issues introduced during
maintenance or expansion.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Feb. 18, 2010

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
from .. import interpreter
from ..interpreter import (
 StatementReturn, StatementExit,
)

#Data-access functions
######################
def get_interpreter(name):
    """
    Provides an interpreter instance, with source identified by ``name``.
    """
    return interpreter.Interpreter(open('processor/test_sources/%(name)s.src' % {
     'name': name,
    }).read())

def execute_no_yield(generator):
    """
    Excecutes a node- or function-`generator` under the assumption that it has no yields.
    
    To repurpose this function for a non-coroutine model, just make this ``pass``, since a
    flow-control exception will be thrown by the called function anyway.
    """
    for prompt in generator:
        generator.send(None)
        
