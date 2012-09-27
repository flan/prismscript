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

from .. import parser
from . import _GenericTestCase

class ConditionalTestCase(_GenericTestCase):
    def test_conditional(self):
        self._test('conditional')
        
    def test_conditional_broken(self):
        self._test_error('conditional_broken', True)
        
    def test_conditional_elif(self):
        self._test('conditional_elif')
        
    def test_conditional_elif_broken(self):
        self._test_error('conditional_elif_broken', True)
        
    def test_conditional_elifs(self):
        self._test('conditional_elifs')
        
    def test_conditional_elifs_broken(self):
        self._test_error('conditional_elifs_broken', True)
        
    def test_conditional_else(self):
        self._test('conditional_else')
        
    def test_conditional_else_broken(self):
        self._test_error('conditional_else_broken', True)
        
    def test_conditional_elif_else(self):
        self._test('conditional_elif_else')
        
    def test_conditional_elif_else_broken(self):
        self._test_error('conditional_elif_else_broken', True)
        
    def test_conditional_nested(self):
        self._test('conditional_nested')
        

class ExpressionListTestCase(_GenericTestCase):
    def test_expressionlist(self):
        self._test('expressionlist')
        
    def test_expressionlist_broken(self):
        self._test_error('expressionlist_broken', True)
        
    def test_expressionlist_broken_2(self):
        self._test_error('expressionlist_broken_2', True)
        

class WhileTestCase(_GenericTestCase):
    def test_while(self):
        self._test('while')
        
    def test_while_break(self):
        self._test('while_break')
        
    def test_while_continue(self):
        self._test('while_continue')
        
    def test_while_nested(self):
        self._test('while_nested')
        
class ForTestCase(_GenericTestCase):
    def test_for(self):
        self._test('for')
        
    def test_for_sequence(self):
        self._test('for_sequence')
        
    def test_for_break(self):
        self._test('for_break')
        
    def test_for_continue(self):
        self._test('for_continue')
        
    def test_for_nested(self):
        self._test('for_nested')
        
