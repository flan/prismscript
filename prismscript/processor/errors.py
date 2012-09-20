import inspect

def get_origin_details():
    return inspect.getframeinfo(inspect.trace()[-1])
    
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
    def __init__(self, location, location_path, message, base_exception):
        self.location_path = [location] + location_path
        self.message = message
        }
        self.base_exception = base_exception
        
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
    
class _StatementCede(FlowControl):
    """
    Indicates that a scope-altering statement was encountered.
    """
    value = None
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return repr(self.value)
        
    def __str__(self):
        return str(self.value)
        
class StatementReturn(_StatementCede):
    """
    Indicates that a ``return`` statement was encountered.
    """
    
class StatementExit(_StatementCede):
    """
    Indicates that an ``exit`` statement was encountered.
    """
    
class StatementsEnd(FlowControl):
    """
    Indicates that the current statement-block has been exhausted normally.
    """
    
