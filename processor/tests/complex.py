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
 get_interpreter,
)

class NestedCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('complex')
        
    def test_iteration_no_conditional(self):
        self.assertEquals(
         self._interpreter.execute_function(
          'conditionals_in_loop', {
           'iterations': 2,
           'else_iterations': 0,
           'x': 2, 'y': 3,
           'break_on_if': False,
           'break_on_elif_1': False,
           'break_on_elif_2': False,
           'break_on_else': False,
          }
         ),
         18
        )
        
    def test_iteration_break_on_if(self):
        self.assertEquals(
         self._interpreter.execute_function(
          'conditionals_in_loop', {
           'iterations': 2,
           'else_iterations': 0,
           'x': 2, 'y': 3,
           'break_on_if': True,
           'break_on_elif_1': False,
           'break_on_elif_2': False,
           'break_on_else': False,
          }
         ),
         6
        )
        
    def test_iteration_break_on_elif_1(self):
        self.assertEquals(
         self._interpreter.execute_function(
          'conditionals_in_loop', {
           'iterations': 2,
           'else_iterations': 0,
           'x': 2, 'y': 3,
           'break_on_if': False,
           'break_on_elif_1': True,
           'break_on_elif_2': False,
           'break_on_else': False,
          }
         ),
         6
        )
        
    def test_iteration_break_on_elif_2(self):
        self.assertEquals(
         self._interpreter.execute_function(
          'conditionals_in_loop', {
           'iterations': 2,
           'else_iterations': 0,
           'x': 2, 'y': 3,
           'break_on_if': False,
           'break_on_elif_1': False,
           'break_on_elif_2': True,
           'break_on_else': False,
          }
         ),
         6
        )
        
    def test_iteration_break_on_else(self):
        self.assertEquals(
         self._interpreter.execute_function(
          'conditionals_in_loop', {
           'iterations': 2,
           'else_iterations': 5,
           'x': 2, 'y': 3,
           'break_on_if': False,
           'break_on_elif_1': False,
           'break_on_elif_2': False,
           'break_on_else': True,
          }
         ),
         21
        )
        
