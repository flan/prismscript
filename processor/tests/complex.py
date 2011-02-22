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
 StatementReturn, StatementExit,
)
import stdlib
import discover_functions

class NestedTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('complex')
        functions = discover_functions.scan(stdlib, '')
        self._interpreter.register_scoped_functions(functions)
        
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
             'else_iterations': 6,
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
            
class CoroutineTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('coroutine')
        
        def coroutine():
            x = yield "Hello!"
            raise StatementReturn(x)
            
        def passive_coroutine():
            x = yield "Hello!"
            
        self._interpreter.register_scoped_functions([
         ('test.coroutine', coroutine),
         ('test.coroutine_passive', passive_coroutine),
        ])
        
    def test_coroutine_node(self):
        try:
            generator = self._interpreter.execute_node('coroutine')
            self.assertEquals(next(generator), 'Hello!')
            generator.send('goodbye')
        except StatementExit as e:
            self.assertEquals(e.value, 'goodbye')
        else:
            self.fail("StatementExit not received")
            
    def test_coroutine_node_noexit(self):
        try:
            generator = self._interpreter.execute_node('coroutine_noexit')
            self.assertEquals(next(generator), 'Hello!')
            generator.send('goodbye')
        except StatementExit as e:
            self.assertEquals(e.value, '')
        else:
            self.fail("StatementExit not received")
            
    def test_coroutine_function(self):
        try:
            generator = self._interpreter.execute_function('coroutine', {})
            self.assertEquals(next(generator), 'Hello!')
            generator.send('goodbye')
        except StatementReturn as e:
            self.assertEquals(e.value, 'goodbye')
        else:
            self.fail("StatementReturn not received")
            
    def test_coroutine_function_noreturn(self):
        try:
            generator = self._interpreter.execute_function('coroutine_noreturn', {})
            self.assertEquals(next(generator), 'Hello!')
            generator.send('goodbye')
        except StatementReturn as e:
            self.assertIsNone(e.value)
        else:
            self.fail("StatementReturn not received")
            
    def test_coroutine_passive_node(self):
        try:
            generator = self._interpreter.execute_node('coroutine_passive')
            self.assertEquals(next(generator), 'Hello!')
            generator.send('goodbye')
        except StatementExit as e:
            self.assertEquals(e.value, '')
        else:
            self.fail("StatementExit not received")
            
    def test_coroutine_passive_node_noexit(self):
        try:
            generator = self._interpreter.execute_node('coroutine_passive_noexit')
            self.assertEquals(next(generator), 'Hello!')
            generator.send('goodbye')
        except StatementExit as e:
            self.assertEquals(e.value, '')
        else:
            self.fail("StatementExit not received")
            
    def test_coroutine_passive_function(self):
        try:
            generator = self._interpreter.execute_function('coroutine_passive', {})
            self.assertEquals(next(generator), 'Hello!')
            generator.send('goodbye')
        except StatementReturn as e:
            self.assertIsNone(e.value)
        else:
            self.fail("StatementReturn not received")
            
    def test_coroutine_passive_function_noreturn(self):
        try:
            generator = self._interpreter.execute_function('coroutine_passive_noreturn', {})
            self.assertEquals(next(generator), 'Hello!')
            generator.send('goodbye')
        except StatementReturn as e:
            self.assertIsNone(e.value)
        else:
            self.fail("StatementReturn not received")
            
