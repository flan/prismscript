"""
interpreter
======
Purpose
-------
Provides a reference interpreter for the language. It's fairly dependent upon the underlying Python
processing model for speed and cleanliness, and it's fail-fast in the event of problems. It keeps
track of the current statement and scope-level to provide some semblance of a traceback in the
event of an exception.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 0.2.0 : Feb. 17, 2011

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
 
 SEQUENCE, ASSIGN_SEQUENCE
 
 FUNCTIONCALL_LOCAL, FUNCTIONCALL_SCOPED, FUNCTIONCALL_UNDEFINED,
 
 #When implementing scoped function-call lookups, be sure to check the first scope-level against
 #the local variables scopes, since they can override the root. (This is important for
 #backwards-compatibility, since it's possible that a new namespace may be reserved after scripts
 #are already using like-named variables, and letting them behave as before is the right thing to
 #do, since they obviously don't need the new functionality)
"""
TOKEN_NAME_MAP = {} #: A reverse-lookup dictionary to get human-readable token identifiers.
for attribute in dir(parser):
    if(attribute.isupper()):
        TOKEN_NAME_MAP[getattr(parser, attribute)] = attribute
#This is a temporary hack meant to speed development. It should NOT be relied upon by any code. EVER.

class Interpreter:
    _functions = None #A dictionary of local functions
    _scoped_functions = None #A dictionary of non-local functions
    _nodes = None #A dictionary of nodes
    _globals = None #A dictionary of global variables
    
    _exit_flag = False #True once an exit-directive has been invoked; causes scopes to break
    _log = None #A high-level execution log to aid debugging
    
    def __init__(self, script):
        """
        Parses the given script and initialises the operating environment.
        
        If the script is invalid, an exception is raised.
        """
        (self._nodes, self._functions) = parser.parse(script)
        self._scoped_functions = {}
        self._globals = {}
        self._log = []
        
    def execute_function(self, function_name, arguments):
        """
        Begins execution of the named function, with the given `arguments`, which are a dictionary
        of parameter-name/value items. The function's parameter-list must match the given arguments.
        
        If a problem occurs, an `ExecutionError` is raised.
        """
        container_name = "%(name)s(%(args)s)" % {
         'name': function_name,
         'args': ', '.join(sorted(arguments.keys())),
        }
        self._log.append("Executing function '%(name)s'..." % {
         'name': container_name,
        })
        
        function = self._functions.get(function_name, frozenset(arguments.keys()))
        if function is None:
            raise FunctionNotFoundError(container_name, "Function not defined")
            
        try:
            self._process_statements(function, seed_locals=arguments)
        except ExecutionError as e:
            raise ExecutionError(container_name, e.location_path, e.message)
        except Exception as e:
            raise ExecutionError(container_name, [], "An unexpected error occurred: %(error)s" % {
             'error': str(e),
            })
            
    def execute_node(self, node_name):
        """
        Begins execution of the named node.
        
        If a problem occurs, an `ExecutionError` is raised.
        """
        self._log.append("Executing node '%(name)s'..." % {
         'name': node_name,
        })
        
        node = self._nodes.get(node_name)
        if node is None:
            raise NodeNotFoundError(node_name, "Node not defined")
            
        try:
            self._process_statements(node)
        except ExecutionError as e:
            raise ExecutionError(node_name, e.location_path, e.message)
        except Exception as e:
            raise ExecutionError(node_name, [], "An unexpected error occurred: %(error)s" % {
             'error': str(e),
            })
            
    def get_log(self):
        """
        Returns the interpreter's execution log, a list of strings, which may be helpful for
        troubleshooting misbehaving scripts.
        """
        return self._log
        
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
        
    def register_scoped_functions(self, functions):
        """
        Makes scoped functions available to the interpreter's operating environment.
        
        `functions` is a sequence of (name:str, function:callable) tuples. Each function is expected
        to accept ``**kwargs`` and handle its own type-marshalling, to facilitate calling functions
        written in other languages or that may have evolving signatures and optional parameters.
        
        Names should be fully qualified and MUST contain at least one scope-delimiter (dot).
        """
        self._scoped_functions.update(dict(functions))
        
    def _assign(self, identifier, expression, _locals):
        """
        Assigns the result of an expression to a local variable, in either the local or global
        scope.
        
        `identifier` is a two-item sequence containing the scope-identifier of the variable and
        its name.
        
        `expression` is the expression to be evaluated.
        
        `_locals` is the current scope's local variables.
        """
        scope = _locals
        if identifier[0] == parser.TERM_IDENTIFIER_LOCAL_GLOBAL:
            scope = self._globals
        scope[identifier[1]] = self._evaluate_expression(expression, _locals)
        
    def _assign_augment(self, identifier, expression, method, _locals):
        """
        Merges the result of an expression with a pre-existing local variable's value, in either the
        local or global scope.
        
        `identifier` is a two-item sequence containing the scope-identifier of the variable and
        its name, `expression` is the expression to be evaluated, and `method` is the type of merge
        to perform.
        
        `_locals` is the current scope's local variables.
        
        If the operation is addition and the expression being added is a string or the value being
        augmented is a string, both terms are converted appropriately.
        """
        scope = _locals
        if identifier[0] == parser.TERM_IDENTIFIER_LOCAL_GLOBAL:
            scope = self._globals
        if not identifier[1] in scope:
            raise VariableNotFoundError(identifier[1], "Local identifier not declared")
            
        expression_result = self._evaluate_expression(expression, _locals)
        if method == parser.ASSIGN_ADD:
            if isinstance(scope[identifier[1]], str) or isinstance(expression_result, str):
                scope[identifier[1]] = ''.join((str(scope[identifier[1]]), str(expression_result)))
            scope[identifier[1]] += expression_result
        elif method == parser.ASSIGN_SUBTRACT:
            scope[identifier[1]] -= expression_result
        elif method == parser.ASSIGN_MULTIPLY:
            scope[identifier[1]] *= expression_result
        elif method == parser.ASSIGN_DIVIDE:
            scope[identifier[1]] /= expression_result
        elif method == parser.ASSIGN_DIVIDE_INTEGER:
            scope[identifier[1]] //= expression_result
            scope[identifier[1]] = int(scope[identifier[1]])
        elif method == parser.ASSIGN_MOD:
            scope[identifier[1]] %= expression_result
            
    def _compare(self, expression_left, expression_right, method, _locals):
        """
        Compares two expressions for logical equality.
        
        `expression_left` and `expression_right` are the expressions to be evaluated and `method` is
        the nature of the test to be performed.
        
        `_locals` is the current scope's local variables.
        
        A boolean value is returned.
        """
        result_left = self._evaluate_expression(expression_left, _locals)
        result_right = self._evaluate_expression(expression_right, _locals)
        if method == parser.TEST_EQUALITY:
            return result_left == result_right
        elif method == parser.TEST_INEQUALITY:
            return result_left != result_right
        elif method == parser.TEST_GREATER_EQUAL:
            return result_left >= result_right
        elif method == parser.TEST_GREATER:
            return result_left > result_right
        elif method == parser.TEST_LESSER_EQUAL:
            return result_left <= result_right
        elif method == parser.TEST_LESSER:
            return result_left < result_right
            
    def _compute(self, expression_left, expression_right, method, _locals):
        """
        Performs a mathematic operation on two expressions.
        
        `expression_left` and `expression_right` are the expressions to be evaluated and `method` is
        the nature of the operation to be performed.
        
        `_locals` is the current scope's local variables.
        
        A numerical value is returned in most cases, though strings can be concatenated through
        addition. If either expression provides a string, the other expression is converted
        appropriately.
        """
        result_left = self._evaluate_expression(expression_left, _locals)
        result_right = self._evaluate_expression(expression_right, _locals)
        if method == parser.MATH_ADD:
            if isinstance(result_left, str) or isinstance(result_right, str):
                return ''.join((str(result_left), str(result_right)))
            return result_left + result_right
        elif method == parser.MATH_SUBTRACT:
            return result_left - result_right
        elif method == parser.MATH_MULTIPLY:
            return result_left * result_right
        elif method == parser.MATH_DIVIDE:
            return result_left / result_right
        elif method == parser.MATH_DIVIDE_INTEGER:
            return int(result_left // result_right)
        elif method == parser.MATH_MOD:
            return result_left % result_right
        elif method == parser.MATH_AND:
            return result_left & result_right
        elif method == parser.MATH_OR:
            return result_left | result_right
        elif method == parser.MATH_XOR:
            return result_left ^ result_right
            
    def _evaluate_expression(self, expression, _locals):
        """
        Evalues an expression and returns a term.
        
        `expression` is the expression to be evaluated.
        
        `_locals` is the current scope's local variables.
        
        If the expression does not have an explicit value, ``None`` is returned.
        """
        if expression[0] in (parser.TERM_BOOL, parser.TERM_STRING, parser.TERM_INTEGER, parser.TERM_FLOAT):
            return expression[1]
        elif expression[0] == parser.TERM_NONE:
            return None
        elif expression[0] == parser.TERM_IDENTIFIER_LOCAL:
            return self._resolve_local_identifier(expression[1], _locals)
        elif expression[0] == parser.TERM_IDENTIFIER_SCOPED: #Only locally-scoped variables may have attributes
            return self._resolve_scoped_identifier(expression[1], _locals)
        elif expression[0] in (
         parser.MATH_MULTIPLY, parser.MATH_DIVIDE, parser.MATH_DIVIDE_INTEGER, parser.MATH_ADD, parser.MATH_SUBTRACT,
         parser.MATH_MOD, parser.MATH_AND, parser.MATH_OR, parser.MATH_XOR
        ):
            return self._compute(expression[1], expression[2], expression[0], _locals)
        elif expression[0] in (
         parser.TEST_EQUALITY, parser.TEST_INEQUALITY,
         parser.TEST_GREATER_EQUAL, parser.TEST_GREATER, parser.TEST_LESSER_EQUAL, parser.TEST_LESSER
        ):
            return self._compare(expression[1], expression[2], expression[0], _locals)
            
    def _process_statements(self, statement_list, scope_locals=None, seed_locals=None):
        """
        Processes all statements within an execution-scope, such as a node, function, or conditional
        wrapper.
        
        `statement_list` is a sequence of statements to be processed in order.
        
        `scope_locals` is an optional dictionary that, if provided, will be used as this scope's
        local variable store, rather than having a new one defined. This is generally expected
        for conditionals.
        
        `seed_locals` is another optional dictionary that can be used to insert arbitrary values
        into the scope's local variable store. This is intended for use when invoking local
        functions, to pass their parameters, but it can also be used to allow for non-destructive
        access to a parent scope's variables, if you're designing a language that should work more
        like C or Java than PHP or Python.
        
        If a problem occurs, an `ExecutionError` is raised.
        """
        self._log.append("Executing statements...")
        
        _locals = {} #A namespace for local variables
        if not scope_locals is None: #This scope is bridged with another, so they should share the same local variables
            _locals = scope_locals
        if not seed_locals is None: #Values were provided to be added to the local variables
            _locals.update(seed_locals)
        for (i, statement) in enumerate(statement_list):
            if self._exit_flag:
                break
                
            try:
                if statement[0] == parser.ASSIGN:
                    self._assign(statement[1], statement[2], _locals)
                elif statement[0] in (
                 parser.ASSIGN_ADD, parser.ASSIGN_SUBTRACT, parser.ASSIGN_MULTIPLY,
                 parser.ASSIGN_DIVIDE, parser.ASSIGN_DIVIDE_INTEGER, parser.ASSIGN_MOD,
                 parser.ASSIGN_SEQUENCE
                ):
                    self._assign_augment(statement[1], statement[2], statement[0], _locals)
                else:
                    print(TOKEN_NAME_MAP[statement[0]])
                    print(statement)
            except ExecutionError as e:
                raise ExecutionError(str(i + 1), e.location_path, e.message)
            except Error as e:
                raise ExecutionError(str(i + 1), [], str(e))
            except Exception as e:
                raise ExecutionError(str(i + 1), [], "An unexpected error occurred: %(error)s" % {
                 'error': str(e),
                })
        print(_locals)
        
    def _resolve_local_identifier(self, identifier, _locals):
        """
        Provides the value of a local identifier by first looking in the local scope, then the
        global scope.
        
        `identifier` is the name of the variable to be retrieved, and `locals` is the current
        scope's local variable store.
        
        A `VariableNotFoundError` is raised if the requested identifier has not been declared.
        """
        if identifier in _locals:
            return _locals[identifier]
        elif identifier in self._globals:
            return self._globals[identifier]
        else:
            raise VariableNotFoundError(identifier, "Local identifier not declared")
            
    def _resolve_scoped_identifier(self, identifier, _locals):
        """
        Provides the value of a scoped identifier.
        
        Since the intent of the language for which this interpreter was written is such that all
        variables have to be bound locally, the root must exist in either the local or global store,
        and the specific target identifier must be a child-attribute of that variable.
        
        Within the context of Python, reflection makes this hierarchy very easy to traverse.
        
        `identifier` is the name of the variable to be retrieved, and `locals` is the current
        scope's local variable store.
        
        A `VariableNotFoundError` is raised if the requested identifier's root has not been
        declared, and `ScopedVariableNotFoundError` is raised if the identifier could not be found
        under the root.
        """
        elements = identifier.split('.')
        variable = None
        try:
            variable = self._resolve_local_identifier(elements[0], _locals)
        except VariableNotFoundError:
            raise ScopedVariableNotFoundError(identifier, "Unable to resolve scoped identifier: root is not a bound local variable")
        if variable is None or type(variable) in (bool, str, int, float):
            raise ScopedVariableNotFoundError(identifier, "Unable to resolve scoped identifier: found a primitive data-type as a local referent")
            
        try:
            for element in elements[1:]:
                variable = getattr(variable, element)
            return variable
        except Exception as e:
            raise ScopedVariableNotFoundError(identifier, "Unable to resolve scoped identifier: %(error)s" % {
             'error': str(e),
            })
            
            
class Error(Exception):
    """
    The base exception from which all exceptions native to this module inherit.
    """
    
class ExecutionError(Error):
    """
    Indicates that an error occurred while executing a statement.
    """
    location_path = None #A path to the location where the error originated.
    message = None #A textual description of the problem.
    def __init__(self, location, location_path, message):
        self.location_path = [location] + location_path
        self.message = message
        
    def __str__(self):
        return "A processing error occurred in [%(path)s]: %(message)s" % {
         'path': ':'.join(self.location_path),
         'message': self.message,
        }
        
class NamespaceLookupError(Error):
    """
    Indicates that the requested namespace element could not be found.
    """
    def __init__(self, identifier, message="No additional information available"):
        Error.__init__(self, "Unable to find '%(identifier)s': %(error)s" % {
         'identifier': identifier,
         'error': message,
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
    
