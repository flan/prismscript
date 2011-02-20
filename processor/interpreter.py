"""
interpreter
======
Purpose
-------
Provides a reference interpreter for the language. It's fairly dependent upon the underlying Python
processing model for speed and cleanliness, and it's fail-fast in the event of problems. It keeps
track of the current statement and scope-level to provide some semblance of a traceback in the
event of an exception.

Notes
-----
At various points in this module, the following anti-pattern will appear::
    generator = <some-generator>
    for prompt in generator:
        generator.send(yield prompt)
        
Another anti-pattern, in the form of flow-control through exceptions, manifests itself for handling
messages that need to transcend scope. Fortunately, they do not pervade outside of this module, and
they are used quite consistently within. They are necessary because it is impossible to both yield
to a co-routine and return an explicit value, so it came down to either having a loose standard of
treating the last-yielded value of a function as its return-value (very, very error-prone and
hard-to-follow) or wrapping them in exception-types and unwrapping them at the appropriate level of
control. Once observed, the process of tracing them should be simple (hint: they're attached to
every coroutine entry-point, which means if you search for 'yield', you'll find them all and know
how to add them when expanding). The overhead associated with exception-handling in Python is
marginal compared to most other languages, owing to its namespace-oriented design, so there's no
real penalty to handling things this way, other than being a bit of a slap in Martin Fowler's face,
but I don't really like his preachy tone anyway. (Even though he's right about most things when
thinking in a Gosling-like mindset, but this is more Kay's domain, so the rules are a fair bit
different)

This is needed to support the coroutine-oriented design of the language this reference interpreter
is meant to provide. The reason for this is that externally registered functions may need to block
for asynchronous events and it's necessary to retain the state of the interpreter's environment
until the event has completed. Building a recursive message-passing chain using generators as
coroutine-handlers seemed like the most externally clean and structurally sound method, but it
added a lot of seemingly duplicated code (that three-line chunk) that, as far as I can fathom,
cannot be simplified, since the generator's evaluation has to take place within the scope of the
executing function. It seems like an acceptable tradeoff, though, since the language will be
primarily extended through library-injection, not syntax/semantics augmentation (automatic Python
type-marshalling makes it easy to define new data-structures and access-methods as language
extensions), so only one or two dedicated maintance programmers will ever be touching this file at a
time.

If you wish to repurpose this interpreter for a simpler, purely synchronous library, most instances
of the anti-pattern can be easily replaced with ``x = <some-generator>``. If you do it right, all
unit tests should pass if you make the indicated changes to ``test_sources/__init__.py`` and disable
the ``coroutine`` testcases in the driver.

Standard usage
--------------
It may seem counter-intuitive, but callers will need to respect the couroutine design and brace
themselves for exceptions used as flow-control mechanisms. (It's cleaner than having a ton of
state-management logic everywhere. Seriously. I would not envy anyone who had to maintain the first
draft).

If calling a node directly::
    node = interpreter.execute_node('my_sweet_node')
    exit_value = None
    try:
        for prompt in node:
            #This could be a series of calls made over a long period of time, rather than a loop.
            if prompt == ('scope.subscope.function', 1): #Some function, somewhere, wants data.
                node.send(prompt[1]) #What you send back is up to your function's needs.
    except StatementExit as e:
        #Not guaranteed to occur; if not encountered, no ``exit`` statement was reached.
        #Node-level ``return`` statements will trigger this, too, for the sake of C/Java
        #programmers.
        exit_value = e.value
        
If calling a function directly::
    function = interpreter.execute_function('my_awesome_function', {'l33t': 1337,})
    return_value = None
    try:
        for prompt in function:
            #This could be a series of calls made over a long period of time, rather than a loop.
            if prompt == ('scope.subscope.function', 1): #Some function, somewhere, wants data.
                node.send(prompt[1]) #What you send back is up to your function's needs.
    except StatementExit as e:
        #This is a subclass of `StatementReturn`, so it can be omitted to munge exit-statement
        #values into the return-value. However, it does have different semantic meaning, in that
        #it indicates an exit statement was reached, rather than a top-level return.
        #
        #This is not guaranteed to occur; if not encountered, no ``exit`` statement was reached
        print(exit_value)
    except StatementReturn as e:
        #This, however, will always occur, unless ``StatementExit`` is encountered.
        return_value = e.value
        
Warning
-------
Before attempting to modify this module, make sure you are well-versed in coroutine theory. Failure
to respect that model will lead to pain. Lots of it. You will cry and people will hate you. It will
be bad.

David Beazley's articles on the subject (and a number of other topics) are pretty comprehensive and
may prove to be a good place to start: http://www.dabeaz.com/coroutines/

He is also, by pure coincidence, the author of the library that handles parsing of the language's
grammar.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 0.9.0 : Feb. 20, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import collections
import re
import types

from .grammar import parser

class Interpreter:
    _functions = None #A dictionary of local functions
    _scoped_functions = None #A dictionary of non-local functions
    _nodes = None #A dictionary of nodes
    _globals = None #A dictionary of global variables
    
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
        
        If the function terminates with a ``return`` statement, the specified value is provided as
        the ``value`` attribute of a raised ``StatementReturn``. This attribute is set to ``None``
        if the statement did not return an explicit value.
        
        If the function cannot be found, `FunctionNotFoundError` is raised.
        
        If a problem occurs, an `ExecutionError` is raised.
        
        If execution terminates with an ``exit`` statement, `StatementExit` is raised and the
        exit-value string may be obtained from its `value` attribute.
        """
        container_name = "%(name)s(%(args)s)" % {
         'name': function_name,
         'args': ', '.join(sorted(arguments.keys())),
        }
        self._log.append("Executing function '%(name)s'..." % {
         'name': container_name,
        })
        
        function = self._functions.get((function_name, frozenset(arguments.keys())))
        if function is None:
            raise FunctionNotFoundError(container_name, "Function not defined")
            
        try:
            prompt = None
            generator = self._process_statements(function, seed_locals=arguments, function=True)
            for prompt in generator:
                x = yield prompt
                generator.send(x)
            raise StatementReturn(prompt)
        except FlowControl:
            raise
        except ExecutionError as e:
            raise ExecutionError(container_name, e.location_path, e.message)
        except Exception as e:
            raise ExecutionError(container_name, [], "An unexpected error occurred: %(error)s" % {
             'error': str(e),
            })
            
    def execute_node(self, node_name):
        """
        Begins execution of the named node.
        
        If the node cannot be found, `NodeNotFoundError` is raised.
        
        If a problem occurs, an `ExecutionError` is raised.
        
        If execution terminates with an ``exit`` statement, `StatementExit` is raised and the
        exit-value string may be obtained from its `value` attribute.
        """
        self._log.append("Executing node '%(name)s'..." % {
         'name': node_name,
        })
        
        node = self._nodes.get(node_name)
        if node is None:
            raise NodeNotFoundError(node_name, "Node not defined")
            
        try:
            self._process_statements(node)
            for prompt in generator:
                x = yield prompt
                generator.send(x)
        except StatementExit:
            raise
        except StatementReturn as e:
            raise StatementExit(e.value)
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
        scope[identifier[1]]
        
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
        
        A ``ValueError`` is raised if the function-list is ill-formed.
        """
        name_re = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)+$')
        for (name, function) in functions: #Validate the list.
            if not type(name) == str:
                raise ValueError("%(name)r is not a string" % {
                 'name': name,
                })
            if not name_re.match(name):
                raise ValueError("'%(name)s' is not a valid scoped identifier" % {
                 'name': name,
                })
            if not isinstance(function, collections.Callable):
                raise ValueError("%(function)r is not a function" % {
                 'function': function,
                })
        self._scoped_functions.update(dict(functions))
        
    def _assign(self, identifier, expression, _locals, evaluate_expression=True):
        """
        Assigns the result of an expression to a local variable, in either the local or global
        scope.
        
        `identifier` is a two-item sequence containing the scope-identifier of the variable and
        its name.
        
        `expression` is the expression to be evaluated.
        
        `_locals` is the current scope's local variables.
        
        If `evaluate_expression` is False, the `expression` is stored directly, without processing.
        This is meant for assigning pre-resolved values.
        """
        scope = self._get_assignment_scope(identifier[0], _locals)
        value = expression
        if evaluate_expression: #Resolve the term
            try:
                generator = self._evaluate_expression(expression, _locals)
                for prompt in generator:
                    x = yield prompt
                    generator.send(x)
            except StatementReturn as e:
                value = e.value
        scope[identifier[1]] = value
        
    def _assign_augment(self, identifier, expression, method, _locals, evaluate_expression=True):
        """
        Merges the result of an expression with a pre-existing local variable's value, in either the
        local or global scope.
        
        `identifier` is a two-item sequence containing the scope-identifier of the variable and
        its name, `expression` is the expression to be evaluated, and `method` is the type of merge
        to perform.
        
        `_locals` is the current scope's local variables.
        
        If `evaluate_expression` is False, the `expression` is stored directly, without processing.
        This is meant for assigning pre-resolved values.
        
        If the operation is addition and the expression being added is a string or the value being
        augmented is a string, both terms are converted appropriately.
        """
        scope = self._get_assignment_scope(identifier[0], _locals)
        if not identifier[1] in scope:
            raise VariableNotFoundError(identifier[1], "Local identifier not declared")
            
        expression_result = expression
        if evaluate_expression: #Resolve the term
            try:
                generator = self._evaluate_expression(expression, _locals)
                for prompt in generator:
                    x = yield prompt
                    generator.send(x)
            except StatementReturn as e:
                expression_result = e.value
                
        if method == parser.ASSIGN_ADD:
            if isinstance(scope[identifier[1]], str) or isinstance(expression_result, str): #Special handling for strings
                scope[identifier[1]] = ''.join((str(scope[identifier[1]]), str(expression_result)))
            else:
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
            
    def _assign_sequence(self, destination, source_expression, _locals):
        """
        Unpacks a Sequence into a series of bound variables.
        
        Variable targets may be local, global, or None. If None, the unpacked counterpart is simply
        discarded.
        
        Sample usage::
            y = [1, 2, 3];
            [x, y, z] = y; //Sets x = 1, y = 2, z = 3.
            
        ValueError is raised if the unpack targets are not acceptable or if a non-sequence is given
        as an unpack-source.
        
        `destination` is a sequence containing unresolved local identifiers or Nones.
        
        `source_expression` is the expression to be evaluated, which must resolve to a Sequence.
        
        `_locals` is the scope's local variable store.
        """
        source = None
        try: #Resolve the sequence
            generator = self._evaluate_expression(source_expression, _locals)
            for prompt in generator:
                x = yield prompt
                generator.send(x)
        except StatementReturn as e: #Expected: occurs in lieu of a return
            source = e.value
            
        if not type(source) == Sequence:
            raise ValueError("Attempted to unpack non-sequence")
            
        unbound_locals = [] #Unpack-target variable-slots that extend beyond the size of the source
        if not len(source) == len(destination):
            self._log.append("Attempted to unpack sequence of length %(source)i into %(destination)i slots" % {
             'source': len(source),
             'destination': len(destination),
            })
            if len(source) > len(destination):
                self._log.append("Destination variables outside the unpack-domain will be bound with a value of None")
                unbound_locals = [v for v in destination[len(source):] if not v[0] == parser.TERM_NONE]
            else:
                self._log.append("Source values outside the unpack-domain will be discarded")
                
        for (identifier, value) in zip(destination, source):
            if identifier[0] == parser.TERM_NONE: #None may be used as a non-assigning placeholder
                continue
                
            if not identifier[0] in (
             parser.TERM_IDENTIFIER_LOCAL,
             parser.TERM_IDENTIFIER_LOCAL_LOCAL, parser.TERM_IDENTIFIER_LOCAL_GLOBAL
            ):
                raise ValueError("Unable to assign value to non-variable in sequence-unpack")
                
            self._assign(identifier, value, _locals, evaluate_expression=False)
            
        for identifier in unbound_locals: #Set anything that was trimmed in the unpack to None to avoid resolution errors
            self._assign(identifier, None, _locals, evaluate_expression=False)
            
    def _compare(self, expression_left, expression_right, method, _locals):
        """
        Compares two expressions for logical equality.
        
        `expression_left` and `expression_right` are the expressions to be evaluated and `method` is
        the nature of the test to be performed.
        
        `_locals` is the current scope's local variables.
        
        A boolean value is returned as the ``value`` attribute of a raised `StatementReturn`.
        """
        #Resolve the left piece's value first, since it can be used for lazy evaluation of booleans.
        result_left = result_right = None
        try: #Resolve the left-hand side
            generator = self._evaluate_expression(expression_left, _locals)
            for prompt in generator:
                x = yield prompt
                generator.send(x)
        except StatementReturn as e: #Expected: occurs in lieu of a return
            result_left = e.value
            
        if method in (parser.TEST_BOOL_OR, parser.TEST_BOOL_AND):
            if method == parser.TEST_BOOL_OR and bool(result_left):
                raise StatementReturn(True)
            elif method == parser.TEST_BOOL_AND and not bool(result_left):
                raise StatementReturn(False)
                
            try: #Resolve the right-hand side
                generator = self._evaluate_expression(expression_right, _locals)
                for prompt in generator:
                    x = yield prompt
                    generator.send(x)
            except StatementReturn as e: #Expected: occurs in lieu of a return
                raise StatementReturn(bool(e.value))
        else: #Lazy evaluation's not a useful option, so evaluate right upfront
            try: #Resolve the right-hand side
                generator = self._evaluate_expression(expression_right, _locals)
                for prompt in generator:
                    x = yield prompt
                    generator.send(x)
            except StatementReturn as e: #Expected: occurs in lieu of a return
                result_right = e.value
                
            if method == parser.TEST_EQUALITY:
                raise StatementReturn(result_left == result_right)
            elif method == parser.TEST_INEQUALITY:
                raise StatementReturn(result_left != result_right)
            elif method == parser.TEST_GREATER_EQUAL:
                raise StatementReturn(result_left >= result_right)
            elif method == parser.TEST_GREATER:
                raise StatementReturn(result_left > result_right)
            elif method == parser.TEST_LESSER_EQUAL:
                raise StatementReturn(result_left <= result_right)
            elif method == parser.TEST_LESSER:
                raise StatementReturn(result_left < result_right)
                
    def _compute(self, expression_left, expression_right, method, _locals):
        """
        Performs a mathematic operation on two expressions.
        
        `expression_left` and `expression_right` are the expressions to be evaluated and `method` is
        the nature of the operation to be performed.
        
        `_locals` is the current scope's local variables.
        
        A numerical value is returned in most cases, though strings can be concatenated through
        addition. If either expression provides a string, the other expression is converted
        appropriately.
        
        The returned value is in the ``value`` attribute of a raised `StatementReturn`.
        """
        #Resolve the left and right pieces' values.
        result_left = result_right = None
        try: #Resolve the left-hand side
            generator = self._evaluate_expression(expression_left, _locals)
            for prompt in generator:
                x = yield prompt
                generator.send(x)
        except StatementReturn as e: #Expected: occurs in lieu of a return
            result_left = e.value
        try: #Resolve the right-hand side
            generator = self._evaluate_expression(expression_right, _locals)
            for prompt in generator:
                x = yield prompt
                generator.send(x)
        except StatementReturn as e: #Expected: occurs in lieu of a return
            result_right = e.value
            
        if method == parser.MATH_ADD:
            if isinstance(result_left, str) or isinstance(result_right, str): #Special handling for strings
                raise StatementReturn(''.join((str(result_left), str(result_right))))
            else:
                raise StatementReturn(result_left + result_right)
        elif method == parser.MATH_SUBTRACT:
            raise StatementReturn(result_left - result_right)
        elif method == parser.MATH_MULTIPLY:
            raise StatementReturn(result_left * result_right)
        elif method == parser.MATH_DIVIDE:
            raise StatementReturn(result_left / result_right)
        elif method == parser.MATH_DIVIDE_INTEGER:
            raise StatementReturn(int(result_left // result_right))
        elif method == parser.MATH_MOD:
            raise StatementReturn(result_left % result_right)
        elif method == parser.MATH_AND:
            raise StatementReturn(result_left & result_right)
        elif method == parser.MATH_OR:
            raise StatementReturn(result_left | result_right)
        elif method == parser.MATH_XOR:
            raise StatementReturn(result_left ^ result_right)
            
    def _evaluate_conditional(self, statement, _locals):
        """
        Processes a conditional-block, executing the appropriate statement-list, if any conditions
        are met.
        
        `statement` is the statement being processed, minus the ``COND_IF`` head and `_locals` is
        the local variable store.
        
        Execution behaviour and exceptions are identical to `_process_statements`.
        """
        statement_list = None
        
        allow = None
        generator = self._evaluate_expression(statement[0][0], _locals)
        try: #Resolve the if-condition's term
            for prompt in generator:
                x = yield prompt
                generator.send(x)
        except StatementReturn as e: #Expected: occurs in lieu of a return
            allow = e.value
            
        if bool(allow):
            statement_list = statement[0][1]
        else:
            for substatement in statement[1:]:
                if substatement[0] == parser.COND_ELIF:
                    generator = self._evaluate_expression(substatement[1], _locals)
                    try: #Resolve the elif-condition's term
                        for prompt in generator:
                            x = yield prompt
                            generator.send(x)
                    except StatementReturn as e: #Expected: occurs in lieu of a return
                        allow = e.value
                        
                    if bool(allow):
                        statement_list = substatement[2]
                        break
                elif substatement[0] == parser.COND_ELSE:
                    statement_list = substatement[1]
                    break
                    
        if statement_list:
            generator = self._process_statements(statement_list, scope_locals=_locals)
            for prompt in generator: #Coroutine boilerplate
                x = yield prompt
                generator.send(x)
                
    def _evaluate_expression(self, expression, _locals):
        """
        Evalues an expression and offers a term.
        
        `expression` is the expression to be evaluated.
        
        `_locals` is the current scope's local variables.
        
        ``StatementReturn`` is raised after the term has been resolved. This is normal; the term's
        value is in its ``value`` attribute.
        """
        expression_type = expression[0]
        
        if expression_type in (parser.TERM_BOOL, parser.TERM_STRING, parser.TERM_INTEGER, parser.TERM_FLOAT):
            raise StatementReturn(expression[1])
        elif expression_type == parser.TERM_NONE:
            raise StatementReturn(None)
        elif expression_type in (
         parser.TERM_IDENTIFIER_LOCAL,
         parser.TERM_IDENTIFIER_LOCAL_LOCAL, parser.TERM_IDENTIFIER_LOCAL_GLOBAL
        ):
            raise StatementReturn(self._resolve_local_identifier(expression[1], _locals, scope=expression_type))
        elif expression_type == parser.TERM_IDENTIFIER_SCOPED: #Only locally-scoped variables may have attributes
            raise StatementReturn(self._resolve_scoped_identifier(expression[1], _locals))
        elif expression_type in (
         parser.MATH_MULTIPLY, parser.MATH_DIVIDE, parser.MATH_DIVIDE_INTEGER, parser.MATH_ADD, parser.MATH_SUBTRACT,
         parser.MATH_MOD, parser.MATH_AND, parser.MATH_OR, parser.MATH_XOR
        ):
            generator = self._compute(expression[1], expression[2], expression_type, _locals)
            for prompt in generator: #Generator is guaranteed to raise a StatementReturn at its end
                x = yield prompt
                generator.send(x)
        elif expression_type in (
         parser.TEST_EQUALITY, parser.TEST_INEQUALITY,
         parser.TEST_GREATER_EQUAL, parser.TEST_GREATER, parser.TEST_LESSER_EQUAL, parser.TEST_LESSER,
         parser.TEST_BOOL_OR, parser.TEST_BOOL_AND
        ):
            generator = self._compare(expression[1], expression[2], expression_type, _locals)
            for prompt in generator: #Generator is guaranteed to raise a StatementReturn at its end
                x = yield prompt
                generator.send(x)
        elif expression_type in (parser.FUNCTIONCALL_LOCAL, parser.FUNCTIONCALL_SCOPED):
            generator = self._invoke_function(expression, _locals)
            for prompt in generator: #Generator is guaranteed to raise a StatementReturn at its end
                x = yield prompt
                generator.send(x)
        elif expression_type == parser.SEQUENCE:
            raise StatementReturn(Sequence([self._evaluate_expression(e, _locals) for e in expression[1]]))
            
        raise ValueError("Unknown expression encountered: %(expression)r" % {
         'expression': expression,
        })
        
    def _execute_local_function(self, function_name, arguments, _locals):
        """
        Attempts to execute the named function with the given `arguments`, which take the form
        of standard ``**kwargs``.
        
        The local variable scopes are searched for bound functions first, to allow users to do
        things like `x = call.play_file;` as a form of short-hand, with the interpreter's namespace
        accessed if no bound variable is found or if the bound variable is not a function (to
        address the case of people used to functions and variables residing in different namespaces,
        as in Java).
        
        `_locals` is the current scope's local variables.
        
        The function's output is returned.
        
        If the function cannot be found, `FunctionNotFoundError` is raised.
        
        Any exceptions raised by the called function are passed through.
        """
        try:
            function = self._resolve_local_identifier(function_name, _locals)
            if isinstance(function, collections.Callable):
                return function(arguments)
            else:
                raise VariableNotFoundError(function_name, "Local identifier is not a bound function")
        except VariableNotFoundError:
            return self.execute_function(function_name, arguments)
            
    def _execute_scoped_function(self, function_name, arguments, _locals):
        """
        Attempts to execute the named function with the given `arguments`, which take the form
        of standard ``**kwargs``.
        
        The local variable scopes are searched for bound functions first, in case the function being
        called is an attribute of a locally bound variable, with the set of registered scoped
        functions accessed afterwards if no bound variable is found. If a bound variable is found at
        the root, but the full path to the named function cannot be resolved, the registered set of
        functions is consulted; this may not be the most expected behaviour, but it will never do
        the wrong thing, unless the author of a script actually wants to make their script fail.
        
        `_locals` is the current scope's local variables.
        
        The function's output is returned.
        
        If the function cannot be found, `ScopedFunctionNotFoundError` is raised.
        
        Any exceptions raised by the called function, or issues like a non-callable variable being
        given parameters, are passed through. 
        """
        try:
            function = self._resolve_scoped_identifier(function_name, _locals)
            if isinstance(function, collections.Callable):
                return function(arguments)
            else:
                raise ScopedVariableNotFoundError(function_name, "Scoped identifier is not a bound function")
        except ScopedVariableNotFoundError:
            function = self._scoped_functions.get(function_name)
            if not function:
                raise ScopedFunctionNotFoundError(function_name, "Function not registered")
            return function(arguments)
            
    def _get_assignment_scope(self, scope_identifier, _locals):
        """
        Returns the scope-variable-store for assignment indicated by the given identifier.
        
        `_locals` is the local variable store.
        """
        if scope_identifier == parser.TERM_IDENTIFIER_LOCAL_GLOBAL:
            return self._globals
        return _locals
        
    def _invoke_function(self, expression, _locals):
        """
        Resolves and executes a function.
        
        `expression` is the expression-body to be processed (scope, name, arguments) and `_locals`
        is the local variable store for resolution purposes.
        
        Any alien types are marshalled into Prismscript-compatible forms.
        
        ``StatementReturn`` is raised after any coroutine execution has completed. This is normal;
        the function's return-value is in its ``value`` attribute.
        """
        result = None
        if expression[0] == parser.FUNCTIONCALL_LOCAL:
            result = self._execute_local_function(expression[1], expression[2], _locals)
        elif expression[0] == parser.FUNCTIONCALL_SCOPED:
            result = self._execute_scoped_function(expression[1], expression[2], _locals)
            
        if type(result) == types.GeneratorType:
            try:
                for prompt in result:
                    x = yield (expression[1], prompt) #Construct a tuple with the identifier of the function in the first slot.
                    result.send(x)
            except StatementReturn as e: #The function is expected to raise a `StatementReturn` if it has a value
                raise StatementReturn(self._marshall_type(e.value))
            raise StatementReturn(None) #None is the standard otherwise.
        else:
            raise StatementReturn(self._marshall_type(result))
            
    def _marshall_type(self, data):
        """
        Coerces `data` received from external sources into equivalent, Prismscript-compatible
        formats.
        """
        if not type(data) == Sequence and isinstance(result, collections.Sequence):
            #Python sequences -> Sequence
            return Sequence(result)
        return result
        
    def _process_statements(self,
     statement_list,
     function=False, while_expression=None,
     scope_locals=None, seed_locals=None
    ):
        """
        Processes all statements within an execution-scope, such as a node, function, or conditional
        wrapper.
        
        `statement_list` is a sequence of statements to be processed in order.
        
        `function` indicates whether this statement-body is directly below a function, meaning that
        a returned value is expected.
        
        `while_expression`, if set, causes a while-loop to be executed until it fails to hold true.
        
        `scope_locals` is an optional dictionary that, if provided, will be used as this scope's
        local variable store, rather than having a new one defined. This is generally expected
        for conditionals.
        
        `seed_locals` is another optional dictionary that can be used to insert arbitrary values
        into the scope's local variable store. This is intended for use when invoking local
        functions, to pass their parameters, but it can also be used to allow for non-destructive
        access to a parent scope's variables, if you're designing a language that should work more
        like C or Java than PHP or Python. (In that case, pass `scope_locals` in here)
        
        If a problem occurs, an `ExecutionError` is raised.
        
        `StatementReturn` will be raised from function contexts and may be raised from non-function
        contexts (conditional bodies, nodes that use ``return`` instead of ``exit``), and
        `StatementExit` will occur if an ``exit`` statement is encountered or control is returned
        after a ``goto`` statement.
        """
        self._log.append("Executing statements...")
        
        _locals = {} #A namespace for local variables
        if not scope_locals is None: #This scope is bridged with another, so they should share the same local variables
            _locals = scope_locals
        if not seed_locals is None: #Values were provided to be added to the local variables
            _locals.update(seed_locals)
            
        _goto_flag = False #True if a goto was encountered, meaning processing should end.
        _while_expression = while_expression
        if not while_expression: #Let the loop execute; this is inverted at the end.
            _while_expression = (parser.TERM_BOOL, True)
        while True:
            generator = self._evaluate_expression(_while_expression, _locals)
            try: #Resolve the while-loop's term
                for prompt in generator:
                    x = yield prompt
                    generator.send(x)
            except StatementReturn as e: #Expected: occurs in lieu of a return
                if not bool(e.value):
                    break
                    
            i = 0 #Statement-enumerator for exception-tracing.
            try:
                for (i, statement) in enumerate(statement_list):
                    statement_type = statement[0]
                    
                    if statement_type == parser.ASSIGN:
                        generator = self._assign(statement[1], statement[2], _locals)
                        for prompt in generator: #Coroutine boilerplate
                            x = yield prompt
                            generator.send(x)
                    elif statement_type in (
                     parser.ASSIGN_ADD, parser.ASSIGN_SUBTRACT, parser.ASSIGN_MULTIPLY,
                     parser.ASSIGN_DIVIDE, parser.ASSIGN_DIVIDE_INTEGER, parser.ASSIGN_MOD,
                    ):
                        generator = self._assign_augment(statement[1], statement[2], statement_type, _locals)
                        for prompt in generator: #Coroutine boilerplate
                            x = yield prompt
                            generator.send(x)
                    elif statement_type == parser.ASSIGN_SEQUENCE:
                        generator = self._assign_sequence(statement[1][1], statement[2], _locals)
                        for prompt in generator: #Coroutine boilerplate
                            x = yield prompt
                            generator.send(x)
                    elif statement_type == parser.STMT_RETURN:
                        generator = self._evaluate_expression(statement[1], _locals)
                        for prompt in generator: #Coroutine boilerplate
                            x = yield prompt
                            generator.send(x)
                        #`_evaluate_expression` is guaranteed to raise `StatementReturn`, so nothing needs to be done here
                    elif statement_type == parser.STMT_GOTO:
                        self.execute_node(statement[1])
                        try:
                            for prompt in generator: #Coroutine boilerplate
                                x = yield prompt
                                generator.send(x)
                        except StatementReturn as e: #Returns from nodes are treated as exits.
                            raise StatementExit(e.value)
                        #If control returns to this point, processing has to end, since a goto is a
                        #break.
                        #Gotos cannot be made non-nested because of the nature of the recursive
                        #message-passing infrastructure needed to support the coroutine model.
                        raise StatementExit('')
                    elif statement_type == parser.COND_IF:
                        generator = self._evaluate_conditional(statement[1:], _locals)
                        for prompt in generator: #Coroutine boilerplate
                            x = yield prompt
                            generator.send(x)
                    elif statement_type == parser.COND_WHILE:
                        generator = self._process_statements(statement[2], while_expression=statement[1], scope_locals=_locals)
                        for prompt in generator: #Coroutine boilerplate
                            x = yield prompt
                            generator.send(x)
                    elif statement_type == parser.STMT_BREAK:
                        raise StatementBreak()
                    elif statement_type == parser.STMT_CONTINUE:
                        raise StatementContinue()
                    elif statement_type == parser.STMT_EXIT:
                        try:
                            generator = self._evaluate_expression(statement[1], _locals)
                            for prompt in generator: #Coroutine boilerplate
                                x = yield prompt
                                generator.send(x)
                        except StatementReturn as e: #Expected: occurs in lieu of a return
                            raise StatementExit(str(e.value))
                    else:
                        try:
                            generator = self._evaluate_expression(statement, _locals)
                            for prompt in generator: #Coroutine boilerplate
                                x = yield prompt
                                generator.send(x)
                        except StatementReturn as e: #Expected, since `_evaluate_expression` always raises one, but it doesn't do anything in this case.
                            pass
            except StatementBreak:
                if not while_expression:
                    raise ExecutionError(str(i + 1), [], "`break` statement not allowed outside of a loop")
                break
            except StatementContinue:
                if not while_expression:
                    raise ExecutionError(str(i + 1), [], "`continue` statement not allowed outside of a loop")
                continue
            except FlowControl: #Allow other control-directives to pass.
                raise
            except ExecutionError as e:
                raise ExecutionError(str(i + 1), e.location_path, e.message)
            except Error as e:
                raise ExecutionError(str(i + 1), [], str(e))
            except Exception as e:
                raise ExecutionError(str(i + 1), [], "An unexpected error occurred: %(error)s" % {
                 'error': str(e),
                })
                
            if not while_expression: #It's not actually a loop, so kill it.
                _while_expression = (parser.TERM_BOOL, False)
                
    def _resolve_local_identifier(self, identifier, _locals, scope=parser.TERM_IDENTIFIER_LOCAL):
        """
        Provides the value of a local identifier by first looking in the local scope, then the
        global scope.
        
        `identifier` is the name of the variable to be retrieved, and `locals` is the current
        scope's local variable store.
        
        `scope` is an optional constant that can be used to narrow the search-scope from the onset.
        
        A `VariableNotFoundError` is raised if the requested identifier has not been declared.
        """
        if scope == parser.TERM_IDENTIFIER_LOCAL: #Search for the proper scope
            if identifier in _locals:
                return _locals[identifier]
            elif identifier in self._globals:
                return self._globals[identifier]
        elif scope == parser.TERM_IDENTIFIER_LOCAL_LOCAL:
            if identifier in _locals:
                return _locals[identifier]
        elif scope == parser.TERM_IDENTIFIER_LOCAL_GLOBAL:
            if identifier in self._globals:
                return self._globals[identifier]
                
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
        if variable is None or type(variable) in (bool, str, int, float, Sequence):
            raise ScopedVariableNotFoundError(identifier, "Unable to resolve scoped identifier: found a primitive data-type as a local referent")
            
        try:
            for element in elements[1:]:
                variable = getattr(variable, element)
            return variable
        except Exception as e:
            raise ScopedVariableNotFoundError(identifier, "Unable to resolve scoped identifier: %(error)s" % {
             'error': str(e),
            })
            
            
class Sequence(list):
    """
    An extension-only subclass of the Python ``list`` type, intended to expose behaviour more
    consistent with Java-like languages and to bypass the lack of access to Python's builtins.
    
    Objects of this type may be passed back to any Python function that expects a sequence.
    """
    def copy(self):
        """
        Returns a shallow copy of this Sequence's items in their current order, so that `sort` and
        `reverse` operations can occur without being destructive.
        """
        return Sequence(self)
        
    def get(self, index):
        """
        Returns the item at the specified `index`.
        """
        return self[index]
        
    def _get_size(self):
        """
        Returns the current number of elements in the sequence.
        """
        return len(self)
    length = property(_get_size)
    
    def pop_head(self):
        """
        Pops an element from the head of the list.
        """
        return self.pop(0)
        
    def pop_tail(self):
        """
        Pops an element from the end of the list.
        """
        return self.pop()
        
    def prepend(self, item):
        """
        Inserts `item` at the head of the sequence.
        """
        self.insert(0, item)
        
        
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
    """str(self._evaluate_expression(statement[1], _locals))
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
    
    
class FlowControl(Exception):
    """
    The base class from which flow-control events inherit.
    """
    
class StatementBreak(FlowControl):
    """
    Indicates that a ``break`` statement was encountered.
    """
    
class StatementContinue(FlowControl):
    """
    Indicates that a ``continue`` statement was encountered.
    """
    
class StatementReturn(FlowControl):
    """
    Indicates that a ``return`` statement was encountered.
    """
    value = None
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return repr(self.value)
        
    def __str__(self):
        return str(self.value)
        
class StatementExit(StatementReturn):
    """
    Indicates that an ``exit`` statement was encountered.
    """
    
