"""
tests.complex
=================
Purpose
-------
Offers support for testing complex structures.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Feb. 18, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import unittest

from . import (
 get_interpreter, execute_no_yield,
 StatementReturn,
)

class NestedTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('complex')
        
    def test_iteration_no_conditional(self):
        try:
            execute_no_yield(self._interpreter.execute_function('conditionals_in_loop', {
             'iterations': 2,
             'else_iterations': 0,
             'x': 2, 'y': 3,
             'break_on_if': False,
             'break_on_elif_1': False,
             'break_on_elif_2': False,
             'break_on_else': False,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 18)
        else:
            self.fail("StatementReturn not received")
            
    def test_iteration_break_on_if(self):
        try:
            execute_no_yield(self._interpreter.execute_function('conditionals_in_loop', {
             'iterations': 2,
             'else_iterations': 0,
             'x': 2, 'y': 3,
             'break_on_if': True,
             'break_on_elif_1': False,
             'break_on_elif_2': False,
             'break_on_else': False,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 6)
        else:
            self.fail("StatementReturn not received")
            
    def test_iteration_break_on_elif_1(self):
        try:
            execute_no_yield(self._interpreter.execute_function('conditionals_in_loop', {
             'iterations': 2,
             'else_iterations': 0,
             'x': 2, 'y': 3,
             'break_on_if': False,
             'break_on_elif_1': True,
             'break_on_elif_2': False,
             'break_on_else': False,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 6)
        else:
            self.fail("StatementReturn not received")
            
    def test_iteration_break_on_elif_2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('conditionals_in_loop', {
             'iterations': 2,
             'else_iterations': 0,
             'x': 2, 'y': 3,
             'break_on_if': False,
             'break_on_elif_1': False,
             'break_on_elif_2': True,
             'break_on_else': False,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 6)
        else:
            self.fail("StatementReturn not received")
            
    def test_iteration_break_on_else(self):
        try:
            execute_no_yield(self._interpreter.execute_function('conditionals_in_loop', {
             'iterations': 2,
             'else_iterations': 5,
             'x': 2, 'y': 3,
             'break_on_if': False,
             'break_on_elif_1': False,
             'break_on_elif_2': False,
             'break_on_else': True,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 21)
        else:
            self.fail("StatementReturn not received")
            
