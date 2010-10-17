"""
tests.expressions
=================
Purpose
-------
Offers the second-most-primitive stage of testing logic for the language, exercising all of its
possible expressions, to make sure that syntactic changes don't mess up any relationships.

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

import parser

import tests

class AssignmentsTestCase(unittest.TestCase):
    def test_assign(self):
        source = tests.get_source('assign')
        (nodes, functions) = tests.get_digest('assign')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_assign_add(self):
        source = tests.get_source('assign_add')
        (nodes, functions) = tests.get_digest('assign_add')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_assign_subtract(self):
        source = tests.get_source('assign_subtract')
        (nodes, functions) = tests.get_digest('assign_subtract')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_assign_multiply(self):
        source = tests.get_source('assign_multiply')
        (nodes, functions) = tests.get_digest('assign_multiply')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_assign_divide(self):
        source = tests.get_source('assign_divide')
        (nodes, functions) = tests.get_digest('assign_divide')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_assign_divide_integer(self):
        source = tests.get_source('assign_divide_integer')
        (nodes, functions) = tests.get_digest('assign_divide_integer')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_assign_sequence(self):
        source = tests.get_source('assign_sequence')
        (nodes, functions) = tests.get_digest('assign_sequence')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

class CommentsTestCase(unittest.TestCase):
    def test_comments(self):
        source = tests.get_source('comments')
        (nodes, functions) = tests.get_digest('comments')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

class FunctionCallsTestCase(unittest.TestCase):
    def test_local(self):
        source = tests.get_source('functioncall_local')
        (nodes, functions) = tests.get_digest('functioncall_local')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_scoped(self):
        source = tests.get_source('functioncall_scoped')
        (nodes, functions) = tests.get_digest('functioncall_scoped')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_undefined(self):
        source = tests.get_source('functioncall_undefined')
        (nodes, functions) = tests.get_digest('functioncall_undefined')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)
        
class MathsTestCase(unittest.TestCase):
    def test_multiply(self):
        source = tests.get_source('math_multiply')
        (nodes, functions) = tests.get_digest('math_multiply')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_divide(self):
        source = tests.get_source('math_divide')
        (nodes, functions) = tests.get_digest('math_divide')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_divide_integer(self):
        source = tests.get_source('math_divide_integer')
        (nodes, functions) = tests.get_digest('math_divide_integer')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_add(self):
        source = tests.get_source('math_add')
        (nodes, functions) = tests.get_digest('math_add')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_subtract(self):
        source = tests.get_source('math_subtract')
        (nodes, functions) = tests.get_digest('math_subtract')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_and(self):
        source = tests.get_source('math_and')
        (nodes, functions) = tests.get_digest('math_and')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_or(self):
        source = tests.get_source('math_or')
        (nodes, functions) = tests.get_digest('math_or')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_nand(self):
        source = tests.get_source('math_nand')
        (nodes, functions) = tests.get_digest('math_nand')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_nor(self):
        source = tests.get_source('math_nor')
        (nodes, functions) = tests.get_digest('math_nor')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_xor(self):
        source = tests.get_source('math_xor')
        (nodes, functions) = tests.get_digest('math_xor')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

class TestsTestCase(unittest.TestCase):
    def test_equality(self):
        source = tests.get_source('test_equality')
        (nodes, functions) = tests.get_digest('test_equality')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_inequality(self):
        source = tests.get_source('test_inequality')
        (nodes, functions) = tests.get_digest('test_inequality')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_greater_equal(self):
        source = tests.get_source('test_greater_equal')
        (nodes, functions) = tests.get_digest('test_greater_equal')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_greater(self):
        source = tests.get_source('test_greater')
        (nodes, functions) = tests.get_digest('test_greater')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_lesser_equal(self):
        source = tests.get_source('test_lesser_equal')
        (nodes, functions) = tests.get_digest('test_lesser_equal')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_lesser(self):
        source = tests.get_source('test_lesser')
        (nodes, functions) = tests.get_digest('test_lesser')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

class SequencesTestCase(unittest.TestCase):
    def test_sequence(self):
        source = tests.get_source('sequence')
        (nodes, functions) = tests.get_digest('sequence')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

class TermsTestCase(unittest.TestCase):
    def test_identifier_local(self):
        source = tests.get_source('term_identifier_local')
        (nodes, functions) = tests.get_digest('term_identifier_local')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_identifier_scoped(self):
        source = tests.get_source('term_identifier_scoped')
        (nodes, functions) = tests.get_digest('term_identifier_scoped')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_none(self):
        source = tests.get_source('term_none')
        (nodes, functions) = tests.get_digest('term_none')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_bool(self):
        source = tests.get_source('term_bool')
        (nodes, functions) = tests.get_digest('term_bool')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_string(self):
        source = tests.get_source('term_string')
        (nodes, functions) = tests.get_digest('term_string')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_integer(self):
        source = tests.get_source('term_integer')
        (nodes, functions) = tests.get_digest('term_integer')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_float(self):
        source = tests.get_source('term_float')
        (nodes, functions) = tests.get_digest('term_float')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

class StatementsTestCase(unittest.TestCase):
    def test_goto(self):
        source = tests.get_source('stmt_goto')
        (nodes, functions) = tests.get_digest('stmt_goto')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_return(self):
        source = tests.get_source('stmt_return')
        (nodes, functions) = tests.get_digest('stmt_return')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

    def test_exit(self):
        source = tests.get_source('stmt_exit')
        (nodes, functions) = tests.get_digest('stmt_exit')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(tests.compare_nodesets(nodes, digest_nodes), None)

