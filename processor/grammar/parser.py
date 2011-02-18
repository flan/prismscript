"""
parser
======
Purpose
-------
Digests a well-formed source file and provides a recursive tree to traverse, making it possible to
bind semantics to an arbitrary encapsulation of language elements.

Using this module, you could build a compiler or interpreter for the language, making it actually do
things.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Oct. 17, 2010

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
from .structure.syntax import parser as _parser
from .structure.syntax import (
 STMT_GOTO, STMT_RETURN, STMT_EXIT,
 STMT_BREAK, STMT_CONTINUE,
 
 COND_IF, COND_ELIF, COND_ELSE,
 COND_WHILE,
 
 TERM_IDENTIFIER_LOCAL, TERM_IDENTIFIER_LOCAL_LOCAL, TERM_IDENTIFIER_LOCAL_GLOBAL,
 TERM_IDENTIFIER_SCOPED,
 TERM_NONE, TERM_BOOL, TERM_STRING, TERM_INTEGER, TERM_FLOAT,
 
 SEQUENCE,
 
 TEST_EQUALITY, TEST_INEQUALITY, TEST_GREATER_EQUAL, TEST_GREATER, TEST_LESSER_EQUAL, TEST_LESSER,
 TEST_BOOL_OR, TEST_BOOL_AND,
 
 MATH_MULTIPLY, MATH_DIVIDE, MATH_DIVIDE_INTEGER, MATH_ADD, MATH_SUBTRACT, MATH_MOD,
 MATH_AND, MATH_OR, MATH_XOR,
 
 FUNCTIONCALL_LOCAL, FUNCTIONCALL_SCOPED, FUNCTIONCALL_UNDEFINED,
 
 ASSIGN, ASSIGN_ADD, ASSIGN_SUBTRACT, ASSIGN_MULTIPLY, ASSIGN_DIVIDE, ASSIGN_DIVIDE_INTEGER,
 ASSIGN_MOD, ASSIGN_SEQUENCE,
)

def parse(source):
    """
    Digests a script as ``source`` and provides a (``nodes``, ``functions``) tuple as output:

    - ``nodes``: A dictionary of ``name``:``expressionlist`` items
    - ``functions``: A dictionary of (``name``, ``parameters``):``expressionlist`` items

    ``name`` is always a string, ``parameters`` is always a frozenset of strings, and
    ``expressionlist`` items are any type of interpretable expression, as described in the
    programming guide.

    An invalid script will never be partially salvaged by this routine. If something is illegal,
    `ValueError` will be raised.
    """
    return _parser.parse(source)
    
