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

:Version: 2.0.0 : Sept. 26, 2012

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import unittest

#Set up a reverse-lookup dictionary by reflecting the parser's namespace.
from .. import parser
TOKEN_NAME_MAP = {} #: A reverse-lookup dictionary to get human-readable token identifiers.
for attribute in dir(parser):
    if(attribute.isupper()):
        TOKEN_NAME_MAP[getattr(parser, attribute)] = attribute

class _GenericTestCase(unittest.TestCase):
    def _test(self, filename):
        source = get_source(filename)
        (nodes, functions) = get_digest(filename)

        (digest_nodes, digest_functions) = parser.parse(source)

        self.assertIsNone(compare_nodesets(digest_nodes, nodes), None)
        self.assertIsNone(compare_nodesets(digest_functions, functions), None)
        
    def _test_error(self, filename, test_nodes):
        source = get_source(filename)
        (nodes, functions) = get_digest(filename)

        (digest_nodes, digest_functions) = parser.parse(source)

        if test_nodes:
            self.assertRaises(
             Error, compare_nodesets,
             nodes, digest_nodes
            )
        else:
            self.assertRaises(
             Error, compare_nodesets,
             functions, digest_functions
            )
            
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
def compare_nodesets(generated, reference):
    """
    A means of comparing two nodesets, either nodes or functions, from two different interpretations
    of the same source.

    ``generated`` and ``reference`` are both node-dictionaries of the appropriate type.

    Exceptions:
    
    - `Error` if a mismatch occurs
    - A native error if a processing problem occurs
    """
    if not generated == reference:
        raise Error("Generated content %(generated)r does not match reference %(reference)s" % {
         'generated': generated,
         'reference': reference,
        })

#Exceptions
###########
class Error(Exception):
    """
    The base class from which all exceptions native to this package inherit.
    """
    
