"""
discover_functions
==================
Purpose
-------
Crawls through modules or objects and constructs Prismscript-interpreter-ready lists of functions to
expose to scripts.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Feb. 20, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import types

def scan(target, base_name, recursive=True, function_list=None):
    """
    Given `target`, which is either a class or an object, and a `base_name` to prepend, with a dot,
    to the name of any discovered functions, this function will crawl through the namespace and find
    every function not prefixed with an underscore.
    
    `recursive`, which is ``True`` by default, may be used to control whether discovered
    module-references should be crawled recursively (this is good if you want to expose a whole
    package).
    
    `function_list` may be a well-formed list of (name, function) pairs. If scanning multiple
    sources sequentially, you may provide the output of one scan as input to another to build a
    single list.
    
    The returned value is a list of (name, function) tuples.
    """
    if function_list is None:
        function_list = []
        
    for element_name in [name for name in dir(target) if not name.startswith('_')]:
        augmented_name = "%(base)s%(delimiter)s%(element)s" % {
         'base': base_name,
         'delimiter': base_name and '.' or '',
         'element': element_name,
        }
        
        element = getattr(target, element_name)
        if type(element) in (types.FunctionType, types.MethodType):
            function_list.append((augmented_name, element))
        elif type(element) == types.ModuleType and recursive:
            scan(element, augmented_name, recursive=recursive, function_list=function_list)
    return function_list
    
