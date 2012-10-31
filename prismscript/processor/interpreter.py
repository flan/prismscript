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
    try:
        prompt = <some-generator>.send(None) #Coroutine boilerplate
        while True:
            x = yield prompt
            prompt = <some-generator>.send(x)
    except StopIteration:
        pass #or bail
        
This is needed to support the coroutine-oriented design of the language this reference interpreter
is meant to provide. The reason for this is that externally registered functions may need to block
for asynchronous events and it's necessary to retain the state of the interpreter's environment
until the event has completed. Building a recursive message-passing chain using generators as
coroutine-handlers seemed like the most externally clean and structurally sound method, but it
added a lot of seemingly duplicated code (that chunk) that, as far as I can fathom, cannot be
simplified, since the generator's evaluation has to take place within the scope of the executing
function. It seems like an acceptable tradeoff, though, since the language will be primarily
extended through library-injection, not syntax/semantics augmentation (automatic Python
type-marshalling makes it easy to define new data-structures and access-methods as language
extensions), so only one or two dedicated maintance programmers will ever be touching this file at a
time.

If you wish to repurpose this interpreter for a simpler, purely synchronous library, most instances
of the anti-pattern can be easily replaced with ``x = <some-generator>``. If you do it right, all
unit tests should pass if you make the indicated changes to ``test_sources/__init__.py`` and disable
the ``coroutine`` testcases in the driver.


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
        prompt = node.send(None)
        while True: #You could spread this out, rather than making it a solid loop
            data = None
            prompt = node.send(data)
    except StatementExit as e:
        #Guaranteed to occur.
        exit_value = e.value
        
If calling a function directly::
    function = interpreter.execute_function('my_awesome_function', {'l33t': 1337,})
    return_value = None
    try:
        prompt = function.send(None)
        while True: #You could spread this out, rather than making it a solid loop
            data = None
            prompt = function.send(data)
    except StatementExit as e:
        #This is not guaranteed to occur; if not encountered, no ``exit`` statement was reached
        print(e.value)
        return
    except StatementReturn as e:
        #This, however, will always occur, unless ``StatementExit`` is encountered.
        return_value = e.value
        
External functions
------------------
For the most part, designing an external function for registration is a simple process: just write
a function as you normally would, give it descriptive parameter-names, and pass it into
`Interpreter.register_scoped_functions()`. You can return a value if you want, including a tuple or
list.

If you want to make use of the coroutine architecture, things are a bit more complex, but they're
not too bad.

In this case, your function needs to be a generator, so it has to ``yield`` a prompt so the
controller knows what to do in response. The identifier used to register your function will
automatically be exposed, so the origin is given for free.

Your function will receive a response, from the calling context (so it's up to you) to its
``yield`` using ``send()``, which can be used to decide how to proceed. Upon completion, your
function may raise an instance of this module's ``StatementReturn`` exception, in the following
way:
``raise prismscript.processor.interpreter.StatementReturn('Your Return Value')``, which will cause
the given value to be returned. Raising ``StopIteration`` is equivalent to raising
``StatementReturn(None)``.

You may return a generator object using the ``StatementReturn`` method, but you cannot return one
using the ``return`` method.

You also have access to ``StatementExit`` to halt execution, but that should generally be left to
script-writers.


Consider using the ``discover_functions`` module to easily build a big list of functions that can be
quickly passed to every new interpreter instance in a sensible format.


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

:Version: 1.0.4 : Sept. 27, 2012


Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import collections
import math
import re
import types

#Python 2.x/3.x compatibility
try: #'long' was replaced by 'int' in py3k
    long
except NameError: #Make them aliases
    long = int
try: #StringTypes were unified in py3k
    types.StringTypes
except AttributeError:
    types.StringTypes = (str,)

from .errors import (
 Error,
 ExecutionError,
 NamespaceLookupError,
 NodeNotFoundError,   
 FunctionNotFoundError, ScopedFunctionNotFoundError,
 VariableNotFoundError, ScopedVariableNotFoundError,
 FlowControl, StatementBreak, StatementContinue,
 StatementReturn, StatementExit,
 StatementsEnd,
 get_origin_details,
)
from .thread_types import (
 ThreadFactory, LockFactory,
)
from .grammar import parser
from .grammar.parser import (
 convert_bool, convert_float, convert_int, convert_string,
 Dictionary, Set, Sequence, String,
)

class Interpreter:
    """
    A shell for interacting with a script in a programmatic manner.
    """
    _functions = None #A dictionary of local functions
    _scoped_functions = None #A dictionary of non-local functions
    _nodes = None #A dictionary of nodes
    _globals = None #A dictionary of global variables
    
    _log = None #A high-level execution log to aid debugging
    
    _loop_limit = 100000 #Limit loop-iterations to 100,000 by default, to hard-break infinite loops

    _lock_factory = None #A lock-factory for concurrency-control primitives
    
    def __init__(self, script, threading=True):
        """
        Parses the given script and initialises the operating environment.
        
        If the script is invalid, an exception is raised.
        
        If `threading` is ``False``, threads and locks will not be enabled and
        will cause exceptions.
        """
        self._nodes = {}
        self._functions = {}
        self.extend_namespace(script)

        self._lock_factory = LockFactory(self)
        self._scoped_functions = {
         'types.bool': convert_bool,
         'types.float': convert_float,
         'types.int': convert_int,
         'types.string': convert_string,
         'types.Dictionary': Dictionary,
         'types.Set': Set,
         'types.Sequence': Sequence,
        }
        if threading:
            self._scoped_functions.update({
             'types.Thread': ThreadFactory(self),
             'types.Lock': self._lock_factory,
            })
            
        self._globals = {}
        
        self._log = []

    @property
    def globals(self):
        """
        Provides the globals dictionary for external analysis or manipulation.

        For safety reasons, this should be accessed only before processing has begun or after it
        has finished, especially if threading is enabled.
        """
        return self._globals
        
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
        exit-value may be obtained from its `value` attribute.
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
            generator = self._process_statements(function, seed_locals=self._marshall_type(arguments), function=True)
            prompt = generator.send(None) #Coroutine boilerplate
            while True:
                x = yield prompt
                prompt = generator.send(x)
        except StatementsEnd:
            raise StatementReturn(None)
        except FlowControl:
            raise
        except ExecutionError as e:
            raise ExecutionError(container_name, e.location_path, e.message, e.base_exception)
        except Exception as e:
            raise ExecutionError(container_name, [], "An unexpected error occurred: %(error)s : %(origin)s" % {
             'error': str(e),
             'origin': get_origin_details(),
            }, e)
        raise StatementReturn(None)
        
    def execute_node(self, node_name):
        """
        Begins execution of the named node.
        
        If the node cannot be found, `NodeNotFoundError` is raised.
        
        If a problem occurs, an `ExecutionError` is raised.
        
        If execution terminates with an ``exit`` statement, `StatementExit` is raised and the
        exit-value may be obtained from its `value` attribute.
        """
        self._log.append("Executing node '%(name)s'..." % {
         'name': node_name,
        })
        
        node = self._nodes.get(node_name)
        if node is None:
            raise NodeNotFoundError(node_name, "Node not defined")
            
        try:
            generator = self._process_statements(node)
            prompt = generator.send(None) #Coroutine boilerplate
            while True:
                x = yield prompt
                prompt = generator.send(x)
        except StatementsEnd:
            raise StatementExit(None) #The end of any node signifies a dead end.
        except StatementExit as e:
            raise StatementExit(e.value)
        except StatementReturn as e: #Not actually legal, but suppressing it would be bad.
            self._log.append("Warning: exit-statement inferred from top-level return.")
            raise StatementExit(e.value)
        except ExecutionError as e:
            raise ExecutionError(node_name, e.location_path, e.message, e.base_exception)
        except Exception as e:
            raise ExecutionError(node_name, [], "An unexpected error occurred: %(error)s : %(origin)s" % {
             'error': str(e),
             'origin': get_origin_details(),
            }, e)
            
    def extend_namespace(self, script):
        """
        Adds the script's nodes and functions to the current namespace.
        
        If the script is invalid, an exception is raised.
        """
        (new_nodes, new_functions) = parser.parse(script)
        self._nodes.update(new_nodes)
        self._functions.update(new_functions)
        
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
            if not type(name) in types.StringTypes:
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

    def release_locks(self, current_thread_is_dead=True):
        """
        Releases all locks provisioned within the interpreter's domain, such that, if the thread
        that acquired a lock no longer exists, the lock goes back to an idle state.

        If `current_thread_is_dead`, the current thread is considered non-existent because it is
        cleaning up, meaning that its locks should be released.

        In general, this method is most useful for internal threads, since interpreter contexts are
        usually discarded after the main node has been followed to completion, but invocation before
        re-entering an interpreter context, with the calling thread considered dead, is not a bad
        or particularly expensive idea, especially compared to the cost of deadlocks due to lazy
        code.

        A list of all offending threads is returned.
        """
        misbehaving_threads = self._lock_factory.release_dead(current_thread_is_dead)
        if misbehaving_threads:
            self._log.append("The following misbehaving threads left locks in use: " + repr(misbehaving_threads))
        return misbehaving_threads
        
    def set_loop_limit(self, limit):
        """
        Sets the loop-iteration-`limit` for hard-breaking infinite loops. A value of 0 will disable
        this feature, but it is not recommended for cases where thread-pools will be involved, since
        an infinite loop will lock a thread, and that could bring down the whole system.
        
        Since this language's primary purpose is to provide a comprehensive, though sandboxed,
        environment for simple control-scripts, it's very possible that someone may, ignorantly or
        maliciously, add a loop that never terminates, killing everything. It's probably better to
        make their script fail than to have productive work halt.
        
        The default limit is 100,000.
        """
        self._loop_limit = limit
        
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
                try:
                    prompt = generator.send(None) #Coroutine boilerplate
                    while True:
                        x = yield prompt
                        prompt = generator.send(x)
                except StopIteration:
                    raise ValueError("Expression did not resolve to a term")
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
        scope = self._identify_assignment_scope(identifier[1], _locals, identifier[0])
        
        expression_result = expression
        if evaluate_expression: #Resolve the term
            try:
                generator = self._evaluate_expression(expression, _locals)
                try:
                    prompt = generator.send(None) #Coroutine boilerplate
                    while True:
                        x = yield prompt
                        prompt = generator.send(x)
                except StopIteration:
                    raise ValueError("Expression did not resolve to a term")
            except StatementReturn as e:
                expression_result = e.value
                
        if method == parser.ASSIGN_ADD:
            if isinstance(scope[identifier[1]], types.StringTypes) or isinstance(expression_result, types.StringTypes): #Special handling for strings
                scope[identifier[1]] = ''.join((str(scope[identifier[1]]), str(expression_result)))
            elif type(scope[identifier[1]]) == Sequence and type(expression_result) == Sequence: #Special handling for sequences
                scope[identifier[1]] = Sequence(scope[identifier[1]] + expression_result)
            else:
                scope[identifier[1]] += expression_result
        elif method == parser.ASSIGN_SUBTRACT:
            scope[identifier[1]] -= expression_result
        elif method == parser.ASSIGN_MULTIPLY:
            scope[identifier[1]] *= expression_result
        elif method == parser.ASSIGN_DIVIDE:
            scope[identifier[1]] /= float(expression_result)
        elif method == parser.ASSIGN_DIVIDE_INTEGER:
            scope[identifier[1]] //= expression_result
            scope[identifier[1]] = int(scope[identifier[1]])
        elif method == parser.ASSIGN_MOD:
            if type(scope[identifier[1]]) == float or type(expression_result) == float:
                scope[identifier[1]] = math.fmod(scope[identifier[1]], expression_result)
            else:
                scope[identifier[1]] %= expression_result
        elif method == parser.ASSIGN_EXPONENTIATE:
            scope[identifier[1]] = math.pow(scope[identifier[1]], expression_result)
            
    def _assign_sequence(self, destination, source_expression, _locals, evaluate_expression=True):
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
        
        `evaluate_expression` may be set to ``False`` if `source_expression` is already a resolved
        sequence.
        """
        source = source_expression
        if evaluate_expression:
            try: #Resolve the sequence
                generator = self._evaluate_expression(source_expression, _locals)
                try:
                    prompt = generator.send(None) #Coroutine boilerplate
                    while True:
                        x = yield prompt
                        prompt = generator.send(x)
                except StopIteration:
                    raise ValueError("Expression did not resolve to a term")
            except StatementReturn as e: #Expected: occurs in lieu of a return
                source = e.value
                
        if not isinstance(source, collections.Sequence):
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
                
            generator = self._assign(identifier, value, _locals, evaluate_expression=False)
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                pass
                
        for identifier in unbound_locals: #Set anything that was trimmed in the unpack to None to avoid resolution errors
            generator = self._assign(identifier, None, _locals, evaluate_expression=False)
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                pass
                
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
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                raise ValueError("Expression did not resolve to a term")
        except StatementReturn as e: #Expected: occurs in lieu of a return
            result_left = e.value
            
        if method in (parser.TEST_BOOL_OR, parser.TEST_BOOL_AND):
            if method == parser.TEST_BOOL_OR and bool(result_left):
                raise StatementReturn(result_left)
            elif method == parser.TEST_BOOL_AND and not bool(result_left):
                raise StatementReturn(result_left)
                
            try: #Resolve the right-hand side
                generator = self._evaluate_expression(expression_right, _locals)
                try:
                    prompt = generator.send(None) #Coroutine boilerplate
                    while True:
                        x = yield prompt
                        prompt = generator.send(x)
                except StopIteration:
                    raise ValueError("Expression did not resolve to a term")
            except StatementReturn as e: #Expected: occurs in lieu of a return
                raise StatementReturn(e.value)
        else: #Lazy evaluation's not a useful option, so evaluate right upfront
            try: #Resolve the right-hand side
                generator = self._evaluate_expression(expression_right, _locals)
                try:
                    prompt = generator.send(None) #Coroutine boilerplate
                    while True:
                        x = yield prompt
                        prompt = generator.send(x)
                except StopIteration:
                    raise ValueError("Expression did not resolve to a term")
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
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                raise ValueError("Expression did not resolve to a term")
        except StatementReturn as e: #Expected: occurs in lieu of a return
            result_left = e.value
        try: #Resolve the right-hand side
            generator = self._evaluate_expression(expression_right, _locals)
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                raise ValueError("Expression did not resolve to a term")
        except StatementReturn as e: #Expected: occurs in lieu of a return
            result_right = e.value
            
        if method == parser.MATH_ADD:
            if isinstance(result_left, types.StringTypes) or isinstance(result_right, types.StringTypes): #Special handling for strings
                raise StatementReturn(''.join((str(result_left), str(result_right))))
            elif type(result_left) == Sequence and type(result_right) == Sequence: #Special handling for sequences
                raise StatementReturn(Sequence(result_left + result_right))
            else:
                raise StatementReturn(result_left + result_right)
        elif method == parser.MATH_SUBTRACT:
            raise StatementReturn(result_left - result_right)
        elif method == parser.MATH_MULTIPLY:
            raise StatementReturn(result_left * result_right)
        elif method == parser.MATH_DIVIDE:
            raise StatementReturn(result_left / float(result_right))
        elif method == parser.MATH_DIVIDE_INTEGER:
            raise StatementReturn(int(result_left // result_right))
        elif method == parser.MATH_MOD:
            if type(result_left) == float or type(result_right) == float:
                raise StatementReturn(math.fmod(result_left, result_right))
            raise StatementReturn(result_left % result_right)
        elif method == parser.MATH_EXPONENTIATE:
            raise StatementReturn(math.pow(result_left, result_right))
            
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
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                raise ValueError("Expression did not resolve to a term")
        except StatementReturn as e: #Expected: occurs in lieu of a return
            allow = e.value
            
        if bool(allow):
            statement_list = statement[0][1]
        else:
            for substatement in statement[1:]:
                if substatement[0] == parser.COND_ELIF:
                    generator = self._evaluate_expression(substatement[1], _locals)
                    try: #Resolve the elif-condition's term
                        try:
                            prompt = generator.send(None) #Coroutine boilerplate
                            while True:
                                x = yield prompt
                                prompt = generator.send(x)
                        except StopIteration:
                            raise ValueError("Expression did not resolve to a term")
                    except StatementReturn as e: #Expected: occurs in lieu of a return
                        allow = e.value
                        
                    if bool(allow):
                        statement_list = substatement[2]
                        break
                elif substatement[0] == parser.COND_ELSE:
                    statement_list = substatement[1]
                    break
                    
        if statement_list:
            generator = self._process_statements(statement_list, scope_locals=_locals, conditional=True)
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                pass
                
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
         parser.MATH_EXPONENTIATE, parser.MATH_MULTIPLY, parser.MATH_DIVIDE,
         parser.MATH_DIVIDE_INTEGER, parser.MATH_ADD, parser.MATH_SUBTRACT, parser.MATH_MOD,
        ):
            generator = self._compute(expression[1], expression[2], expression_type, _locals)
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                raise ValueError("StatementReturn not received")
        elif expression_type in (
         parser.TEST_EQUALITY, parser.TEST_INEQUALITY,
         parser.TEST_GREATER_EQUAL, parser.TEST_GREATER, parser.TEST_LESSER_EQUAL, parser.TEST_LESSER,
         parser.TEST_BOOL_OR, parser.TEST_BOOL_AND
        ):
            generator = self._compare(expression[1], expression[2], expression_type, _locals)
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                raise ValueError("StatementReturn not received")
        elif expression_type in (parser.FUNCTIONCALL_LOCAL, parser.FUNCTIONCALL_SCOPED):
            generator = self._invoke_function(expression, _locals)
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                raise ValueError("StatementReturn not received")
        elif expression_type == parser.TEST_NEGATE:
            generator = self._evaluate_expression(expression[1], _locals)
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                raise ValueError("StatementReturn not received")
            except StatementReturn as e:
                raise StatementReturn(not e.value)
        elif expression_type == parser.SUFFIX:
            generator = self._evaluate_expression(expression[1], _locals)
            try:
                prompt = generator.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = generator.send(x)
            except StopIteration:
                raise ValueError("StatementReturn not received")
            except StatementReturn as e:
                target = e.value
                for token in expression[2][1].split('.'):
                    target = getattr(target, token)
                if expression[2][0] == parser.TERM_IDENTIFIER_SUFFIX:
                    raise StatementReturn(self._marshall_type(target))
                elif expression[2][0] == parser.FUNCTIONCALL_SUFFIX:
                    generator = self._invoke_function((expression[2][0], target, expression[2][2]), _locals)
                    try:
                        prompt = generator.send(None) #Coroutine boilerplate
                        while True:
                            x = yield prompt
                            prompt = generator.send(x)
                    except StopIteration:
                        raise ValueError("StatementReturn not received")
        elif expression_type == parser.SEQUENCE:
            sequence = []
            for e in expression[1]:
                generator = self._evaluate_expression(e, _locals)
                try:
                    try:
                        prompt = generator.send(None) #Coroutine boilerplate
                        while True:
                            x = yield prompt
                            prompt = generator.send(x)
                    except StopIteration:
                        raise ValueError("Expression did not resolve to a term")
                except StatementReturn as e:
                    sequence.append(e.value)
            raise StatementReturn(Sequence(sequence))
            
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
                return function(**arguments)
            else:
                raise VariableNotFoundError(function_name, "Local identifier is not a bound function")
        except VariableNotFoundError:
            return self.execute_function(function_name, arguments)
        raise FunctionNotFoundError("Unable to find local function %(name)s(%(parameters)s)" % {
         'name': function_name,
         'parameters': ', '.join(arguments.keys()),
        })
        
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
                return function(**arguments)
            else:
                raise ScopedVariableNotFoundError(function_name, "Scoped identifier is not a bound function")
        except ScopedVariableNotFoundError:
            function = self._scoped_functions.get(function_name)
            if not function:
                raise ScopedFunctionNotFoundError(function_name, "Function not registered")
            return function(**arguments)
        raise ScopedFunctionNotFoundError("Unable to find scoped function %(name)s(%(parameters)s)" % {
         'name': function_name,
         'parameters': ', '.join(arguments.keys()),
        })
        
    def _get_assignment_scope(self, scope_identifier, _locals):
        """
        Returns the scope-variable-store for assignment indicated by the given identifier.
        
        `_locals` is the local variable store.
        """
        if scope_identifier == parser.TERM_IDENTIFIER_LOCAL_GLOBAL:
            return self._globals
        return _locals

    def _identify_assignment_scope(self, identifier, _locals, scope=parser.TERM_IDENTIFIER_LOCAL):
        """
        Provides the scope of a local identifier by first looking for it in the local scope, then
        the global scope.
        
        `identifier` is the name of the variable to be retrieved, and `_locals` is the current
        scope's local variable store.
        
        `scope` is an optional constant that can be used to narrow the search-scope from the onset.
        
        A `VariableNotFoundError` is raised if the requested identifier has not been declared.
        """
        if scope == parser.TERM_IDENTIFIER_LOCAL: #Search for the proper scope
            if identifier in _locals:
                return _locals
            elif identifier in self._globals:
                return self._globals
        elif scope == parser.TERM_IDENTIFIER_LOCAL_LOCAL:
            if identifier in _locals:
                return _locals
        elif scope == parser.TERM_IDENTIFIER_LOCAL_GLOBAL:
            if identifier in self._globals:
                return self._globals

        raise VariableNotFoundError(identifier, "Local identifier not declared")
        
    def _invoke_function(self, expression, _locals):
        """
        Resolves and executes a function.
        
        `expression` is the expression-body to be processed (scope, name, arguments) and `_locals`
        is the local variable store for resolution purposes.
        
        Any alien types are marshalled into Prismscript-compatible forms.
        
        ``StatementReturn`` is raised after any coroutine execution has completed. This is normal;
        the function's return-value is in its ``value`` attribute.
        """
        arguments = {}
        for (argument, expr) in expression[2].items():
            generator = self._evaluate_expression(expr, _locals)
            try:
                try:
                    prompt = generator.send(None) #Coroutine boilerplate
                    while True:
                        x = yield prompt
                        prompt = generator.send(x)
                except StopIteration:
                    raise ValueError("Argument-expression did not resolve to a term")
            except StatementReturn as e: #Guaranteed to happen
                arguments[argument] = e.value
                
        self._log.append("Invoking function '%(name)s(%(args)s)'..." % {
         'name': expression[1],
         'args': ', '.join(sorted(arguments.keys())),
        })
        
        result = None
        try:
            if expression[0] == parser.FUNCTIONCALL_LOCAL:
                result = self._execute_local_function(expression[1], arguments, _locals)
            elif expression[0] == parser.FUNCTIONCALL_SCOPED:
                result = self._execute_scoped_function(expression[1], arguments, _locals)
            elif expression[0] == parser.FUNCTIONCALL_SUFFIX:
                result = expression[1](**arguments)
        except StatementReturn as e:
            raise StatementReturn(self._marshall_type(e.value))
            
        if type(result) == types.GeneratorType:
            try:
                prompt = result.send(None) #Coroutine boilerplate
                while True:
                    x = yield prompt
                    prompt = result.send(x)
            except StopIteration: #Let None be returned.
                pass
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
        if not type(data) == String and isinstance(data, types.StringTypes):
            #Python strings/unicodes -> String
            return String(data)
        elif not type(data) in (Sequence, String) and isinstance(data, collections.Sequence):
            #Python sequences -> Sequence
            return Sequence((self._marshall_type(d) for d in data))
        elif not type(data) == Dictionary and isinstance(data, collections.Mapping):
            #Python mappings -> Dictionary
            return Dictionary(((self._marshall_type(k), self._marshall_type(v)) for (k, v) in data.items()))
        elif not type(data) == Set and isinstance(data, collections.Set):
            #Python sets -> Set
            return Set((self._marshall_type(d) for d in data))
        return data
        
    def _process_statements(self,
     statement_list,
     function=False,
     foreach_identifier=None, foreach_iterable=None,
     while_expression=None,
     conditional=False,
     scope_locals=None, seed_locals=None
    ):
        """
        Processes all statements within an execution-scope, such as a node, function, or conditional
        wrapper.
        
        `statement_list` is a sequence of statements to be processed in order.
        
        `function` indicates whether this statement-body is directly below a function, meaning that
        a returned value is expected.
        
        `foreach_identifier` is a local identifier to which the next item from `foreach_iterable`
        will be assigned. If ``None`` (the default), a foreach-loop will not be executed.
        
        `foreach_iterable` is an iterable that will be consumed for assignment into the
        `foreach_identifier`. If ``None`` (the default), a foreach-loop will not be executed.
        
        `while_expression`, if set, causes a while-loop or foreach-loop to be executed until it
        fails to hold true or it has been exhausted.
        
        `conditional` indicates whether this is running in a conditional context.
        
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
        if not while_expression is None and foreach_identifier:
            raise ValueError("A while-loop cannot also be a foreach-loop -- this is a design issue")
            
        if not while_expression is None:
            self._log.append("Entering while-loop...")
        elif not foreach_iterable is None:
            self._log.append("Entering foreach-loop...")
        elif function:
            self._log.append("Entering function...")
        else:
            self._log.append("Entering node...")
            
        _locals = {} #A namespace for local variables
        if not scope_locals is None: #This scope is bridged with another, so they should share the same local variables
            _locals = scope_locals
        if not seed_locals is None: #Values were provided to be added to the local variables
            _locals.update(seed_locals)
            
        _foreach_iterable = None
        if not foreach_iterable is None:
            _foreach_iterable = iter(foreach_iterable)
            
        _while_expression = while_expression
        if while_expression is None: #Let the loop execute; this is inverted at the end.
            _while_expression = (parser.TERM_BOOL, True)
        iteration_count = 0
        while True:
            if self._loop_limit and self._loop_limit < iteration_count:
                self._log.append("Hard-breaking loop for exceeding iteration-limit of %(limit)i cycles" % {
                 'limit': self._loop_limit,
                })
                break
                
            if _foreach_iterable and foreach_identifier: #Definitely a foreach-loop
                generator = None
                try:
                    if foreach_identifier[0] == parser.SEQUENCE:
                        generator = self._assign_sequence(foreach_identifier[1], next(_foreach_iterable), _locals, evaluate_expression=False)
                    else:
                        generator = self._assign(foreach_identifier, next(_foreach_iterable), _locals, evaluate_expression=False)
                except StopIteration: #Iterator's exhausted
                    break
                try:
                    prompt = generator.send(None) #Coroutine boilerplate
                    while True:
                        x = yield prompt
                        prompt = generator.send(x)
                except StopIteration:
                    pass
            elif foreach_identifier:
                raise ValueError("A foreach-loop cannot iterate over a non-collection")
            else: #Possibly a while-loop
                generator = self._evaluate_expression(_while_expression, _locals)
                try: #Resolve the while-loop's term
                    try:
                        prompt = generator.send(None) #Coroutine boilerplate
                        while True:
                            x = yield prompt
                            prompt = generator.send(x)
                    except StopIteration:
                        pass
                except StatementReturn as e: #Expected: occurs in lieu of a return
                    if not bool(e.value):
                        break
                        
            i = 0 #Statement-enumerator for exception-tracing.
            try:
                for (i, statement) in enumerate(statement_list):
                    statement_type = statement[0]
                    
                    if statement_type == parser.ASSIGN:
                        generator = self._assign(statement[1], statement[2], _locals)
                        try:
                            prompt = generator.send(None) #Coroutine boilerplate
                            while True:
                                x = yield prompt
                                prompt = generator.send(x)
                        except StopIteration:
                            pass
                    elif statement_type in (
                     parser.ASSIGN_ADD, parser.ASSIGN_SUBTRACT, parser.ASSIGN_EXPONENTIATE,
                     parser.ASSIGN_MULTIPLY, parser.ASSIGN_DIVIDE, parser.ASSIGN_DIVIDE_INTEGER,
                     parser.ASSIGN_MOD,
                    ):
                        generator = self._assign_augment(statement[1], statement[2], statement_type, _locals)
                        try:
                            prompt = generator.send(None) #Coroutine boilerplate
                            while True:
                                x = yield prompt
                                prompt = generator.send(x)
                        except StopIteration:
                            pass
                    elif statement_type == parser.ASSIGN_SEQUENCE:
                        generator = self._assign_sequence(statement[1][1], statement[2], _locals)
                        try:
                            prompt = generator.send(None) #Coroutine boilerplate
                            while True:
                                x = yield prompt
                                prompt = generator.send(x)
                        except StopIteration:
                            pass
                    elif statement_type == parser.STMT_RETURN:
                        generator = self._evaluate_expression(statement[1], _locals)
                        try:
                            prompt = generator.send(None) #Coroutine boilerplate
                            while True:
                                x = yield prompt
                                prompt = generator.send(x)
                        except StopIteration:
                            raise ValueError("StatementReturn not received")
                    elif statement_type == parser.STMT_GOTO:
                        generator = self.execute_node(statement[1])
                        try:
                            prompt = generator.send(None) #Coroutine boilerplate
                            while True:
                                x = yield prompt
                                prompt = generator.send(x)
                        except StopIteration:
                            raise StatementsEnd()
                    elif statement_type == parser.COND_IF:
                        try:
                            generator = self._evaluate_conditional(statement[1:], _locals)
                            try:
                                prompt = generator.send(None) #Coroutine boilerplate
                                while True:
                                    x = yield prompt
                                    prompt = generator.send(x)
                            except StopIteration:
                                pass
                        except StatementsEnd:
                            pass
                    elif statement_type == parser.COND_WHILE:
                        try:
                            generator = self._process_statements(statement[2], while_expression=statement[1], scope_locals=_locals)
                            try:
                                prompt = generator.send(None) #Coroutine boilerplate
                                while True:
                                    x = yield prompt
                                    prompt = generator.send(x)
                            except StopIteration:
                                pass
                        except StatementsEnd:
                            pass
                    elif statement_type == parser.COND_FOR:
                        try:
                            generator = self._evaluate_expression(statement[2], _locals)
                            try:
                                try:
                                    prompt = generator.send(None) #Coroutine boilerplate
                                    while True:
                                        x = yield prompt
                                        prompt = generator.send(x)
                                except StopIteration:
                                    raise ValueError("StatementReturn not received")
                            except StatementReturn as e:
                                generator = self._process_statements(statement[3], foreach_identifier=statement[1], foreach_iterable=e.value, scope_locals=_locals)
                                try:
                                    prompt = generator.send(None) #Coroutine boilerplate
                                    while True:
                                        x = yield prompt
                                        prompt = generator.send(x)
                                except StopIteration:
                                    pass
                        except StatementsEnd:
                            pass
                    elif statement_type == parser.STMT_BREAK:
                        raise StatementBreak()
                    elif statement_type == parser.STMT_CONTINUE:
                        raise StatementContinue()
                    elif statement_type == parser.STMT_EXIT:
                        try:
                            generator = self._evaluate_expression(statement[1], _locals)
                            try:
                                prompt = generator.send(None) #Coroutine boilerplate
                                while True:
                                    x = yield prompt
                                    prompt = generator.send(x)
                            except StopIteration:
                                raise ValueError("StatementReturn not received")
                        except StatementReturn as e:
                            raise StatementExit(e.value)
                    else:
                        try:
                            generator = self._evaluate_expression(statement, _locals)
                            try:
                                prompt = generator.send(None) #Coroutine boilerplate
                                while True:
                                    x = yield prompt
                                    prompt = generator.send(x)
                            except StopIteration:
                                raise ValueError("StatementReturn not received")
                        except StatementReturn as e:
                            pass
            except StatementBreak:
                if conditional:
                    raise
                elif not while_expression and not foreach_identifier:
                    raise ExecutionError(str(i + 1), [], "`break` statement not allowed outside of a loop", None)
                break
            except StatementContinue:
                if conditional:
                    raise
                elif not while_expression and not foreach_identifier:
                    raise ExecutionError(str(i + 1), [], "`continue` statement not allowed outside of a loop", None)
                continue
            except StatementReturn:
                raise
            except StatementExit: #Allow exits to pass.
                raise
            except ExecutionError as e:
                raise ExecutionError(str(i + 1), e.location_path, e.message, e.base_exception)
            except Error as e:
                raise ExecutionError(str(i + 1), [], str(e), e)
            except Exception as e:
                raise ExecutionError(str(i + 1), [], "An unexpected error occurred: %(error)s : %(origin)s | locals: %(locals)r | globals: %(globals)r" % {
                 'error': str(e),
                 'origin': get_origin_details(),
                 'locals': sorted(_locals.items()),
                 'globals': sorted(self._globals.items()),
                }, e)
                
            if not while_expression: #It's not actually a loop, so kill it. This is benign in the case of a foreach.
                _while_expression = (parser.TERM_BOOL, False)
            iteration_count += 1
            
        raise StatementsEnd()
        
    def _resolve_local_identifier(self, identifier, _locals, scope=parser.TERM_IDENTIFIER_LOCAL):
        """
        Provides the value of a local identifier by first looking in the local scope, then the
        global scope.
        
        `identifier` is the name of the variable to be retrieved, and `_locals` is the current
        scope's local variable store.
        
        `scope` is an optional constant that can be used to narrow the search-scope from the onset.
        
        A `VariableNotFoundError` is raised if the requested identifier has not been declared.
        """
        return self._identify_assignment_scope(identifier, _locals, scope)[identifier]
        
    def _resolve_scoped_identifier(self, identifier, _locals):
        """
        Provides the value of a scoped identifier.
        
        Since the intent of the language for which this interpreter was written is such that all
        variables have to be bound locally, the root must exist in either the local or global store,
        and the specific target identifier must be a child-attribute of that variable. If no root
        binding is provided, the scoped functions table is consulted as a fall-back.
        
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
            scoped_function = self._scoped_functions.get(identifier) #See if it's a reference to a scoped function.
            if scoped_function:
                return scoped_function
            raise ScopedVariableNotFoundError(identifier, "Unable to resolve scoped identifier: root is not a bound local variable")
        if variable is None or type(variable) in (bool, int, long, float) or type(variable) in types.StringTypes:
            raise ScopedVariableNotFoundError(identifier, "Unable to resolve scoped identifier: found a primitive data-type as a local referent")
            
        try:
            for element in elements[1:]:
                variable = getattr(variable, element)
            return variable
        except Exception as e:
            raise ScopedVariableNotFoundError(identifier, "Unable to resolve scoped identifier: %(error)s" % {
             'error': str(e),
            })
            
