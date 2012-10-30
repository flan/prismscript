"""
tests.conditionals
=================
Purpose
-------
Offers support for testing conditionals.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Feb. 20, 2011

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

class IfTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('conditionals')
        
    def test_if_true(self):
        try:
            execute_no_yield(self._interpreter.execute_function('if_true', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_if_false(self):
        try:
            execute_no_yield(self._interpreter.execute_function('if_false', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 0)
        else:
            self.fail("StatementReturn not received")
            
    def test_elif_true(self):
        try:
            execute_no_yield(self._interpreter.execute_function('elif_true', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 2)
        else:
            self.fail("StatementReturn not received")
            
    def test_elif_false(self):
        try:
            execute_no_yield(self._interpreter.execute_function('elif_false', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 0)
        else:
            self.fail("StatementReturn not received")
            
    def test_elif2_true(self):
        try:
            execute_no_yield(self._interpreter.execute_function('elif2_true', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 4)
        else:
            self.fail("StatementReturn not received")
            
    def test_elif2_false(self):
        try:
            execute_no_yield(self._interpreter.execute_function('elif2_false', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 0)
        else:
            self.fail("StatementReturn not received")
            
    def test_if_else(self):
        try:
            execute_no_yield(self._interpreter.execute_function('if_else', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 2)
        else:
            self.fail("StatementReturn not received")
            
    def test_if_elif_else(self):
        try:
            execute_no_yield(self._interpreter.execute_function('if_elif_else', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 4)
        else:
            self.fail("StatementReturn not received")
            
    def test_if_elif2_else(self):
        try:
            execute_no_yield(self._interpreter.execute_function('if_elif2_else', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 8)
        else:
            self.fail("StatementReturn not received")
            
    def test_if_true_else(self):
        try:
            execute_no_yield(self._interpreter.execute_function('if_true_else', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_elif_true_else(self):
        try:
            execute_no_yield(self._interpreter.execute_function('elif_true_else', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 2)
        else:
            self.fail("StatementReturn not received")
            
    def test_elif2_true_else(self):
        try:
            execute_no_yield(self._interpreter.execute_function('elif2_true_else', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 4)
        else:
            self.fail("StatementReturn not received")
            
    def test_if_exit(self):
        try:
            execute_no_yield(self._interpreter.execute_node('if_exit'))
        except StatementExit as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementExit not received")
            
    def test_if_return(self):
        try:
            execute_no_yield(self._interpreter.execute_function('if_return', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementReturn not received")
            
class WhileTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('conditionals')
        
    def test_while(self):
        try:
            execute_no_yield(self._interpreter.execute_function('_while', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_while_exit(self):
        try:
            execute_no_yield(self._interpreter.execute_node('while_exit'))
        except StatementExit as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementExit not received")
            
    def test_while_return(self):
        try:
            execute_no_yield(self._interpreter.execute_function('while_return', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementReturn not received")
            
    def test_while_return(self):
        try:
            execute_no_yield(self._interpreter.execute_function('while_return', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementReturn not received")
            
    def test_while_break(self):
        try:
            execute_no_yield(self._interpreter.execute_function('while_break', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_while_break_conditional(self):
        try:
            execute_no_yield(self._interpreter.execute_function('while_break_conditional', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 6)
        else:
            self.fail("StatementReturn not received")
            
    def test_while_continue(self):
        try:
            execute_no_yield(self._interpreter.execute_function('while_continue', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_while_continue_conditional(self):
        try:
            execute_no_yield(self._interpreter.execute_function('while_continue_conditional', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
            
class ForTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('conditionals')
        
    def test_for(self):
        try:
            execute_no_yield(self._interpreter.execute_function('_for', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_for_sequence(self):
        try:
            execute_no_yield(self._interpreter.execute_function('_for_sequence', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (2, 12))
        else:
            self.fail("StatementReturn not received")
            
    def test_for_exit(self):
        try:
            execute_no_yield(self._interpreter.execute_node('for_exit'))
        except StatementExit as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementExit not received")
            
    def test_for_return(self):
        try:
            execute_no_yield(self._interpreter.execute_function('for_return', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementReturn not received")
            
    def test_for_return(self):
        try:
            execute_no_yield(self._interpreter.execute_function('for_return', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementReturn not received")
            
    def test_for_break(self):
        try:
            execute_no_yield(self._interpreter.execute_function('for_break', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_for_break_conditional(self):
        try:
            execute_no_yield(self._interpreter.execute_function('for_break_conditional', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 3)
        else:
            self.fail("StatementReturn not received")
            
    def test_for_continue(self):
        try:
            execute_no_yield(self._interpreter.execute_function('for_continue', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_for_continue_conditional(self):
        try:
            execute_no_yield(self._interpreter.execute_function('for_continue_conditional', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_for_in_none(self):
        self.assertRaises(
         Exception, execute_no_yield,
         self._interpreter.execute_function('for_in_none', {})
        )
        
