"""
interpreter
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
from .grammar import parser
"""
 STMT_GOTO, STMT_RETURN, STMT_EXIT,
 STMT_BREAK, STMT_CONTINUE,
 
 COND_IF, COND_ELIF, COND_ELSE,
 COND_WHILE,
 
 TERM_IDENTIFIER_LOCAL, TERM_IDENTIFIER_SCOPED, TERM_NONE, TERM_BOOL, TERM_STRING, TERM_INTEGER,
 TERM_FLOAT,
 
 SEQUENCE,
 
 TEST_EQUALITY, TEST_INEQUALITY, TEST_GREATER_EQUAL, TEST_GREATER, TEST_LESSER_EQUAL, TEST_LESSER,
 
 MATH_MULTIPLY, MATH_DIVIDE, MATH_DIVIDE_INTEGER, MATH_ADD, MATH_SUBTRACT, MATH_MOD,
 MATH_AND, MATH_OR, MATH_NAND, MATH_NOR,
 
 FUNCTIONCALL_LOCAL, FUNCTIONCALL_SCOPED, FUNCTIONCALL_UNDEFINED,
 
 ASSIGN, ASSIGN_ADD, ASSIGN_SUBTRACT, ASSIGN_MULTIPLY, ASSIGN_DIVIDE, ASSIGN_DIVIDE_INTEGER,
 ASSIGN_MOD, ASSIGN_SEQUENCE,
"""

class Interpreter:
    _nodes = None #A dictionary of nodes
    _functions = None #A dictionary of functions
    _globals = None #A dictionary of global variables
    
    def __init__(self, script):
        (nodes, functions, structure) = parser.parse(script)
        self._nodes = nodes
        self._functions = functions
        
        self._globals = {}
        
    def execute_node(self, node_name):
        node = self._nodes.get(node_name)
        if node is None:
            raise NodeNotFoundError(node_name)
            
        locals = {} #A namespace for local variables
        for statement in self._nodes[node_name]:
            print(statement)
            
    def list_functions(self):
        """
        Provides a list of all functions defined within the interpreter's local environment.
        
        The value returned is a sequence of names coupled with sets containing lists of named
        parameters.
        """
        return self._functions.keys()
        
    def list_nodes(self):
        """
        Provides a list of all nodes defined within the interpreter's local environment.
        
        The value returned is a sequence of names.
        """
        return self._nodes.keys()
        
        
class Error(Exception):
    """
    The base exception from which all exceptions native to this module inherit.
    """
    
class NamespaceLookupError(Error):
    """
    Indicates that the requested namespace element could not be found.
    """
    def __init__(self, identifier, message="No additional information available"):
        Error.__init__(self, "Unable to find '%(identifier)s': %(error)s" % {
         'identifier': identifier,
         'message': message,
        })
        
class NodeNotFoundError(NamespaceLookupError):
    """
    Indicates that the requested node was not found.
    """
    
class FunctionNotFoundError(NamespaceLookupError):
    """
    Indicates that the requested local function was not found.
    """
    
class ScopedFunctionNotFoundError(FunctionNotFoundError):
    """
    Indicates that the requested scoped function was not found.
    """
    
class VariableNotFoundError(NamespaceLookupError):
    """
    Indicates that the requested variable was not found.
    """
    
class ScopedVariableNotFoundError(VariableNotFoundError):
    """
    Indicates that the requested scoped variable was not found.
    """
    
