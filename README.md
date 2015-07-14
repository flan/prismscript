Prismscript is an I/O-control-centric language intended to simplify the process of decoupling instructions and application logic from processing machinery.

# History #
Originally, Prismscript was devised to allow for scene-scripting in the now-defunct Summer Prisms visual novel project, to provide a safe sandboxed context that would enable scenario-writers to create rich experiences without exposing the client's system to the usual degree of risk associated with executing untrusted code. Since then, the language has found applications in commercial contexts, too, as a means of powering procedural behaviour-flows.

The evolution of the language is documented on [uguu.ca](http://uguu.ca/tag/prismscript/).

# Overview #
Prismscript's syntax is based on PHP with some Python-like enhancements and it runs on any platform capable of supporting David Beazly's excellent [PLY](http://www.dabeaz.com/ply/), under either Python 2.6+ or Py3k. It can be integrated into a Python application in a manner almost as simple as calling a function and it does not attempt to take control of your design's infrastructure in any way: prepare modules or objects that contain functions you would like to expose to the interpreter's context, run the scanning function over them, and then tell the interpreter which entry-point you'd like it to execute; it does everything internally.

It also ships with a fairly rich (and easy to extend) standard library, which you can optionally load, in whole or in part, into an interpreter's context. In addition to that, it includes useful data-structures from Python, wrapped to be usable in the language's less-expressive syntax.

It is entirely based on coroutines, not subroutines, allowing for a great deal of flexibility in applications that perform complex tasks in discrete chunks: single-threaded/thread-pooled progress-based scheduling is useful in more cases than you might expect.

## Sample ##
**Note:** for full details, please see the [wiki](../../wiki)

### Prismscript ###
```
node{ #Calls a function twice and then exits with the result as a string
    x = function(x=2);
    y = function(x=3);
    z = [x, y];
    
    exit lang.string.join(s=z, glue=' < '); //Returns '4.0 < 9.0'
}

function(x){ #Just squares the given number
    return math.pow(v=x, exponent=2);
}
```

### Python ###
```
import prismscript.processor.interpreter as prismscript_interpreter
import prismscript.stdlib
import prismscript.discover_functions
interpreter = prismscript_interpreter.Interpreter(string_with_code_from_previous_section)
interpreter.register_scoped_functions(prismscript.discover_functions.scan(prismscript.stdlib, ''))

node = interpreter.execute_node('node')
exit_value = None
try:
    prompt = node.send(None) #Start execution of the coroutine; may yield a value
    while True: #The loop could be external, allowing a threadpool to make a single pass at the prompt before waiting for user input or something
       #Act on `prompt` to decide what to send back
       data = None
       prompt = node.send(data) #Send the message back in and get the next yielded value for processing
except prismscript_interpreter.StatementExit as e:
    #Guaranteed to occur.
    exit_value = e.value
```


---

# Contacts #
red {dot} hamsterx {at} gmail
