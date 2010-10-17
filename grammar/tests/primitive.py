"""
tests.primitive
===============
Purpose
-------
Offers the most primitive battery of tests for the language, ensuring that nodes and functions can
be declared and referenced and that they can hold expression-lists.

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
import unittest

from . import parser
from . import (
 get_source, get_digest, compare_nodesets,
 SignatureInconsistencyError,
)

class FunctionTestCase(unittest.TestCase):
    def test_function(self):
        source = get_source('function')
        (nodes, functions) = get_digest('function')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)

    def test_function_broken(self):
        source = get_source('function_broken')
        (nodes, functions) = get_digest('function_broken')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         SignatureInconsistencyError, compare_nodesets,
         functions, digest_functions
        )

    def test_function_broken_2(self):
        source = get_source('function_broken_2')
        (nodes, functions) = get_digest('function_broken_2')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         SignatureInconsistencyError, compare_nodesets,
         functions, digest_functions
        )
        
    def test_function_expressions(self):
        source = get_source('function_expressions')
        (nodes, functions) = get_digest('function_expressions')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(functions, digest_functions), None)


class NamespaceTestCase(unittest.TestCase):
    def test_namespace(self):
        source = get_source('namespace')
        (nodes, functions) = get_digest('namespace')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)
        self.assertEquals(compare_nodesets(functions, digest_functions), None)

    def test_namespace_broken_function(self):
        source = get_source('namespace_broken_function')
        (nodes, functions) = get_digest('namespace_broken_function')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)
        self.assertRaises(
         SignatureInconsistencyError, compare_nodesets,
         functions, digest_functions
        )

    def test_namespace_broken_function_signature(self):
        source = get_source('namespace_broken_function_signature')
        (nodes, functions) = get_digest('namespace_broken_function_signature')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)
        self.assertRaises(
         SignatureInconsistencyError, compare_nodesets,
         functions, digest_functions
        )

    def test_namespace_broken_node(self):
        source = get_source('namespace_broken_node')
        (nodes, functions) = get_digest('namespace_broken_node')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         SignatureInconsistencyError, compare_nodesets,
         nodes, digest_nodes
        )
        self.assertEquals(compare_nodesets(functions, digest_functions), None)


class NodeTestCase(unittest.TestCase):
    def test_node(self):
        source = get_source('node')
        (nodes, functions) = get_digest('node')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)

    def test_node_broken(self):
        source = get_source('node_broken')
        (nodes, functions) = get_digest('node_broken')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         SignatureInconsistencyError, compare_nodesets,
         nodes, digest_nodes
        )
        
    def test_node_expressions(self):
        source = get_source('node_expressions')
        (nodes, functions) = get_digest('node_expressions')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)


