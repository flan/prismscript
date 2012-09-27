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

:Version: 1.0.2 : Sept. 26, 2012

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import unittest

from .. import parser
from . import _GenericTestCase

class AssignmentsTestCase(_GenericTestCase):
    def test_assign(self):
        self._test('assign')
        
    def test_assign_add(self):
        self._test('assign_add')
        
    def test_assign_divide(self):
        self._test('assign_divide')
        
    def test_assign_divide_integer(self):
        self._test('assign_divide_integer')
        
    def test_assign_mod(self):
        self._test('assign_mod')
        
    def test_assign_multiply(self):
        self._test('assign_multiply')
        
    def test_assign_sequence(self):
        self._test('assign_sequence')
        
    def test_assign_subtract(self):
        self._test('assign_subtract')
        

class CommentsTestCase(_GenericTestCase):
    def test_comments(self):
        self._test('comments')
        
        
class FunctionCallsTestCase(_GenericTestCase):
    def test_local(self):
        self._test('functioncall_local')
        
    def test_scoped(self):
        self._test('functioncall_scoped')
        

class SuffixExpressionsTestCase(_GenericTestCase):
    def test_scoped_suffix_identifier(self):
        self._test('functioncall_scoped_suffix_identifier')
        
    def test_scoped_suffix_identifier_2(self):
        self._test('functioncall_scoped_suffix_identifier_2')
        
    def test_scoped_suffix_call(self):
        self._test('functioncall_scoped_suffix_call')
        
    def test_scoped_suffix_call_2(self):
        self._test('functioncall_scoped_suffix_call_2')
        
    def test_scoped_suffix_call_identifier(self):
        self._test('functioncall_scoped_suffix_call_identifier')
        
    def test_scoped_suffix_call_call(self):
        self._test('functioncall_scoped_suffix_call_call')
        
    def test_suffix_term_call(self):
        self._test('suffix_term_call')
        
    def test_suffix_term_identifier(self):
        self._test('suffix_term_identifier')
        
        
class MathsTestCase(_GenericTestCase):
    def test_add(self):
        self._test('math_add')
        
    def test_exponentiate(self):
        self._test('math_exponentiate')
        
    def test_divide(self):
        self._test('math_divide')
        
    def test_divide_integer(self):
        self._test('math_divide_integer')
        
    def test_mod(self):
        self._test('math_mod')
        
    def test_multiply(self):
        self._test('math_multiply')
        
    def test_subtract(self):
        self._test('math_subtract')
        
        
class SequencesTestCase(_GenericTestCase):
    def test_sequence(self):
        self._test('sequence')
        

class StatementsTestCase(_GenericTestCase):
    def test_exit(self):
        self._test('stmt_exit')
        
    def test_goto(self):
        self._test('stmt_goto')
        
    def test_return(self):
        self._test('stmt_return')
        
        
class TermsTestCase(_GenericTestCase):
    def test_bool(self):
        self._test('term_bool')
        
    def test_float(self):
        self._test('term_float')
        
    def test_identifier_local(self):
        self._test('term_identifier_local')
        
    def test_identifier_local_qualified(self):
        self._test('term_identifier_local_qualified')
        
    def test_identifier_scoped(self):
        self._test('term_identifier_scoped')
        
    def test_integer(self):
        self._test('term_integer')
        
    def test_none(self):
        self._test('term_none')
        
    def test_string(self):
        self._test('term_string')
        

class TestsTestCase(_GenericTestCase):
    def test_equality(self):
        self._test('test_equality')
        
    def test_greater(self):
        self._test('test_greater')
        
    def test_greater_equal(self):
        self._test('test_greater_equal')
        
    def test_inequality(self):
        self._test('test_inequality')
        
    def test_lesser(self):
        self._test('test_lesser')
        
    def test_lesser_equal(self):
        self._test('test_lesser_equal')
        
    def test_bool_and(self):
        self._test('test_bool_and')
        
    def test_bool_or(self):
        self._test('test_bool_or')
        
    def test_negate(self):
        self._test('test_negate')
        
