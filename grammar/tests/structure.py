"""
tests.structure
===============
Purpose
-------
Offers the third level of unit testing, ensuring that the language's control structures
(expression-lists and conditionals) operate as expected.

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
 ConditionalInconsistencyError, ExpressionInconsistencyError, ExpressionListInconsistencyError,
)

class ExpressionListTestCase(unittest.TestCase):
    def test_expressionlist(self):
        source = get_source('expressionlist')
        (nodes, functions) = get_digest('expressionlist')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)

    def test_expressionlist_broken(self):
        source = get_source('expressionlist_broken')
        (nodes, functions) = get_digest('expressionlist_broken')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         ExpressionInconsistencyError, compare_nodesets,
         nodes, digest_nodes
        )

    def test_expressionlist_broken_2(self):
        source = get_source('expressionlist_broken_2')
        (nodes, functions) = get_digest('expressionlist_broken_2')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         ExpressionListInconsistencyError, compare_nodesets,
         nodes, digest_nodes
        )

class ConditionalTestCase(unittest.TestCase):
    def test_conditional(self):
        source = get_source('conditional')
        (nodes, functions) = get_digest('conditional')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)

    def test_conditional_broken(self):
        source = get_source('conditional_broken')
        (nodes, functions) = get_digest('conditional_broken')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         ExpressionInconsistencyError, compare_nodesets,
         nodes, digest_nodes
        )
        
    def test_conditional_elif(self):
        source = get_source('conditional_elif')
        (nodes, functions) = get_digest('conditional_elif')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)

    def test_conditional_elif_broken(self):
        source = get_source('conditional_elif_broken')
        (nodes, functions) = get_digest('conditional_elif_broken')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         ExpressionInconsistencyError, compare_nodesets,
         nodes, digest_nodes
        )
        
    def test_conditional_elifs(self):
        source = get_source('conditional_elifs')
        (nodes, functions) = get_digest('conditional_elifs')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)

    def test_conditional_elifs_broken(self):
        source = get_source('conditional_elifs_broken')
        (nodes, functions) = get_digest('conditional_elifs_broken')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         ConditionalInconsistencyError, compare_nodesets,
         nodes, digest_nodes
        )
        
    def test_conditional_else(self):
        source = get_source('conditional_else')
        (nodes, functions) = get_digest('conditional_else')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)

    def test_conditional_else_broken(self):
        source = get_source('conditional_else_broken')
        (nodes, functions) = get_digest('conditional_else_broken')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         ConditionalInconsistencyError, compare_nodesets,
         nodes, digest_nodes
        )

    def test_conditional_elif_else(self):
        source = get_source('conditional_elif_else')
        (nodes, functions) = get_digest('conditional_elif_else')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)

    def test_conditional_elif_else_broken(self):
        source = get_source('conditional_elif_else_broken')
        (nodes, functions) = get_digest('conditional_elif_else_broken')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertRaises(
         ExpressionInconsistencyError, compare_nodesets,
         nodes, digest_nodes
        )

    def test_conditional_nested(self):
        source = get_source('conditional_nested')
        (nodes, functions) = get_digest('conditional_nested')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)
        
