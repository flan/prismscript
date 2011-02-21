import types

def scan(target, base_name, recursive=True, function_list=None):
    if function_list is None:
        function_list = []
        
    for element_name in [name for name in dir(target) if not name.startswith('_')]: #Check every non-private attribute
        augmented_name = "%(base)s.%(element)s" % {
         'base': base_name,
         'element': element_name,
        }
        
        element = getattr(target, element_name)
        if type(element) == types.FunctionType:
            function_list.append((augmented_name, element))
        elif type(element) == types.ModuleType and recursive:
            scan_module(element, augmented_name, recursive=recursive, function_list=function_list)
    return function_list
    
