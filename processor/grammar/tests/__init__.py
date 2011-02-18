"""
tests (package)
===============
Purpose
-------
Provides test-oriented access to the language's grammar, allowing for a high degree of
semantics-free introspection and analysis to support rapid diagnosis of issues introduced during
maintenance or expansion.

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
#Set up a reverse-lookup dictionary by reflecting the parser's namespace.
from .. import parser
TOKEN_NAME_MAP = {} #: A reverse-lookup dictionary to get human-readable token identifiers.
for attribute in dir(parser):
    if(attribute.isupper()):
        TOKEN_NAME_MAP[getattr(parser, attribute)] = attribute

#Data-access functions
######################
def get_digest(name):
    """
    Provides a previously serialized digest of a source script, identified by ``name``.

    A pair of dictionaries, one of nodes and one of functions, is returned.
    """
    digest = open('grammar/test_sources/%(name)s.dgst' % {
     'name': name,
    })
    nodes = eval(digest.readline())
    functions = eval(digest.readline())
    return (nodes, functions)

def get_source(name):
    """
    Provides a source script, identified by ``name``.

    The returned value is a string.
    """
    return open('grammar/test_sources/%(name)s.src' % {
     'name': name,
    }).read()


#Testing functions
##################
def compare_assignments(generated, reference):
    """
    Compares two assignments, to see if they are equal.

    ``generated`` and ``reference`` are both assignments of any valid type.

    Exceptions:

    - If the assignments' targets are non-equal, `TermInconsistencyError` is raised.
    - If the assignmnets' values are non-equal, a child of `ExpressionInconsistencyError`
      is raised.
    """
    if not generated[1] == reference[1]:
        raise TermInconsistencyError("Local identifier %(generated)s not equal to %(reference)s" % {
         'generated': generated[1],
         'reference': reference[1],
        })
    compare_expressions(generated[2], reference[2])

def compare_conditionals(generated, reference):
    """
    Compares two conditional structures, to see if they are equal.

    ``generated`` and ``reference`` are both conditional entry-points.

    Exceptions:

    - If the structure of the conditionals is non-equal, `ConditionalInconsistencyError` is raised.
    - If the conditionals' qualifiers or directives are non-equal,
      `ExpressionListInconsistencyError` or a child of `ExpressionInconsistencyError` is raised.
    """
    compare_expressions(generated[1][0], reference[1][0])
    compare_expression_lists(generated[1][1], reference[1][1])
    generated = generated[2:]
    reference = reference[2:]

    while generated and reference:
        g = generated.pop(0)
        r = reference.pop(0)
        if g == r: #Python recursively compares all native data-types by default.
            continue

        compare_types(g, r)
        if g[0] == parser.COND_ELIF:
            compare_expressions(g[1], r[1])
            compare_expression_lists(g[2], r[2])
        elif g[0] == parser.COND_ELSE:
            compare_expression_lists(g[1], r[1])
    if generated:
        raise ConditionalInconsistencyError("Additional elements in generated: %(elements)s" % {
         'elements': generated,
        })
    if reference:
        raise ConditionalInconsistencyError("Additional elements in reference: %(elements)s" % {
         'elements': reference,
        })

def compare_expressions(generated, reference):
    """
    Compares two expressions, to see if they are equal.

    ``generated`` and ``reference`` are both expressions of any valid type.

    Exceptions:

    - If the expressions are non-equal, a child of `ExpressionInconsistencyError` is raised.
    """
    if TOKEN_NAME_MAP[generated[0]].startswith('TERM'):
        compare_terms(generated, reference)
    elif TOKEN_NAME_MAP[generated[0]].startswith('SEQUENCE'):
        compare_sequences(generated, reference)
    elif TOKEN_NAME_MAP[generated[0]].startswith('FUNCTIONCALL'):
        compare_functioncalls(generated, reference)
    elif TOKEN_NAME_MAP[generated[0]].startswith('TEST'):
        compare_tests(generated, reference)
    elif TOKEN_NAME_MAP[generated[0]].startswith('MATH'):
        compare_maths(generated, reference)

def compare_expression_lists(generated, reference):
    """
    A means of ensuring that two expressionlists are identical.

    ``generated`` and ``reference`` are both expressionlists.

    Exceptions:
    
    - If one expressionlist is longer than the other, `ExpressionListInconsistencyError` is raised.
    - Any other exception from this module may be raised on an appropriate trigger, with the
      omission of `SignatureInconsistencyError`; this parent-function invokes everything else.
    """
    while generated and reference:
        g = generated.pop(0)
        r = reference.pop(0)
        if g == r: #Python recursively compares all native data-types by default.
            continue

        compare_types(g, r)
        if g[0] == parser.COND_IF:
            compare_conditionals(g, r)
        elif TOKEN_NAME_MAP[g[0]].startswith('ASSIGN'):
            compare_assignments(g, r)
        elif TOKEN_NAME_MAP[g[0]].startswith('STMT'):
            compare_statements(g, r)
        else:
            compare_expressions(g, r)
    if generated:
        raise ExpressionListInconsistencyError("Additional elements in generated: %(elements)s" % {
         'elements': generated,
        })
    if reference:
        raise ExpressionListInconsistencyError("Additional elements in reference: %(elements)s" % {
         'elements': reference,
        })

def compare_functioncalls(generated, reference):
    """
    Compares two functioncalls, to see if they are equal.

    ``generated`` and ``reference`` are both functioncalls of any valid type.

    Exceptions:

    - If the targets are non-equal, `FunctionCallInconsistencyError` is raised.
    - If the parameters are non-equal, `FunctionCallParametersInconsistencyError` is raised.
    - If the arguments are non-equal, a child of `ExpressionInconsistencyError` is raised.
    """
    if generated[0] == parser.FUNCTIONCALL_UNDEFINED:
        if not generated[1] == reference[1]:
            raise TermInconsistencyError("Local identifier %(generated)s not equal to %(reference)s" % {
             'generated': generated[1],
             'reference': reference[1],
            })
    else:
        if not generated[1] == reference[1]:
            raise FunctionCallInconsistencyError("FunctionCall %(generated)s not equal to %(reference)s" % {
             'generated': generated[1],
             'reference': reference[1],
            })

        generated_kwarg_paramaters = set(generated[2].keys())
        reference_kwarg_paramaters = set(reference[2].keys())
        if generated_kwarg_paramaters.symmetric_difference(reference_kwarg_paramaters):
            raise FunctionCallParametersInconsistencyError("%(functioncall)s parameters %(generated)s not equal to %(reference)s" % {
             'functioncall': generated[1],
             'generated': sorted(generated_kwarg_paramaters),
             'reference': sorted(reference_kwarg_paramaters),
            })

        for (paramater, argument) in generated[2]:
            compare_expressions(argument, reference[2].get(paramater))

def compare_maths(generated, reference):
    """
    Compares two math-expressions, to see if they are equal.

    ``generated`` and ``reference`` are both math-expressions of any valid type.

    Exceptions:

    - If the left- and right-hand sides are non-equal, a child of `ExpressionInconsistencyError` is
      raised.
    """
    compare_expressions(generated[1], reference[1])
    compare_expressions(generated[2], reference[2])

def compare_nodesets(generated, reference):
    """
    A means of comparing two nodesets, either nodes or functions, from two different interpretations
    of the same source.

    ``generated`` and ``reference`` are both node-dictionaries of the appropriate type.

    Exceptions:
    
    - Any exception from this module may be raised on an appropriate trigger; this parent-function
      invokes everything else.
    """
    compare_node_signatures(generated, reference)

    for (signature, expressionlist) in generated.items():
        compare_expression_lists(expressionlist[:], reference[signature][:])
        
def compare_node_signatures(generated, reference):
    """
    A means of comparing the signatures of sets of nodes or functions.

    ``generated`` and ``reference`` are both node-dictionaries of the appropriate type.

    Exceptions:
    
    - If the two sets are inconsistent, `SignatureInconsistencyError` is raised.
    """
    generated_names = set(generated.keys())
    reference_names = set(reference.keys())
    
    differences = generated_names.symmetric_difference(reference_names)
    if differences:
        summaries = []
        reference_missing = reference_names.difference(generated_names)
        if reference_missing:
            summaries.append("defined only in reference: %(names)s" % {
             'names': sorted(reference_missing),
            })
        generated_missing = generated_names.difference(reference_names)
        if generated_missing:
            summaries.append("defined only in generated: %(names)s" % {
             'names': sorted(generated_missing),
            })
        raise SignatureInconsistencyError("Inconsistencies in signatures: %(summary)s" % {
         'summary': ';'.join(summaries),
        })

def compare_sequences(generated, reference):
    """
    Compares two sequences, to see if they are equal.

    ``generated`` and ``reference`` are both sequences of any valid type.

    Exceptions:

    - If the sequences are non-equal, `SequenceInconsistencyError` is raised.
    """
    if not generated[1] == reference[1]:
        raise SequenceInconsistencyError("Sequence %(generated)s not equal to %(reference)s" % {
         'generated': generated[1],
         'reference': reference[1],
        })

def compare_statements(generated, reference):
    """
    Compares two statements, to see if they are equal.

    ``generated`` and ``reference`` are both statements of any valid type.

    Exceptions:

    - If the statements' arguments are non-equal, a child of `ExpressionInconsistencyError` is raised.
    """
    compare_expressions(generated[1], reference[1])
    
def compare_terms(generated, reference):
    """
    Compares two terms, to see if they are equal.

    ``generated`` and ``reference`` are both terms of any valid type.

    Exceptions:

    - If the terms are non-equal, `TermInconsistencyError` is raised.
    """
    if not generated[1] == reference[1]:
        raise TermInconsistencyError("Term %(generated)s not equal to %(reference)s" % {
         'generated': generated[1],
         'reference': reference[1],
        })

def compare_tests(generated, reference):
    """
    Compares two tests, to see if they are equal.

    ``generated`` and ``reference`` are both tests of any valid type.

    Exceptions:

    - If the left- and right-hand sides are non-equal, a child of `ExpressionInconsistencyError` is
      raised.
    """
    compare_expressions(generated[1], reference[1])
    compare_expressions(generated[2], reference[2])

def compare_types(generated, reference):
    """
    Compares two types, to see if their contents can be further contrasted.

    ``generated`` and ``reference`` are both non-top-level items.

    Exceptions:

    - If the types are incompatible, `ExpressionInconsistencyError` is raised.
    """
    if not generated[0] == reference[0]:
        raise ExpressionInconsistencyError("Incompatible types: %(generated_type)s and %(reference_type)s, covering %(generated)s and %(reference)s" % {
         'generated_type': TOKEN_NAME_MAP[generated[0]],
         'reference_type': TOKEN_NAME_MAP[reference[0]],
         'generated': generated[1:],
         'reference': reference[1:],
        })


#Exceptions
###########
class ConditionalInconsistencyError(Exception):
    """
    Indicates that two conditional structures are different.
    """
    
class ExpressionInconsistencyError(Exception):
    """
    Indicates that two expressions are irreconcilably different, in cases where more specifc
    inconsistency errors aren't applicalbe.
    """
    
class ExpressionListInconsistencyError(Exception):
    """
    Indicates that two expressionlists have irreconcilable differences, such as differences in
    length.
    """
    
class FunctionCallInconsistencyError(ExpressionInconsistencyError):
    """
    Indicates that two function calls refer to different targets.
    """

class FunctionCallParametersInconsistencyError(ExpressionInconsistencyError):
    """
    Indicates that two function calls have different keyword argument parameters.
    """

class SequenceInconsistencyError(ExpressionInconsistencyError):
    """
    Indicates that two sequences have different values.
    """

class SignatureInconsistencyError(Exception):
    """
    Indicates that the signatures of two nodesets are inconsistent.
    """

class TermInconsistencyError(ExpressionInconsistencyError):
    """
    Indicates that two terms have different values.
    """
    
