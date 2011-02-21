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
 StatementExit,
)

class SimpleTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('nodes')
        
        def test():
            return 82
            
        self._interpreter.register_scoped_functions([('test.test', test)])
        
    def test_simple(self):
        try:
            execute_no_yield(self._interpreter.execute_node('simple'))
        except StatementExit as e:
            self.assertEquals(e.value, '')
        else:
            self.fail("StatementExit not received")
        
    def test_goto(self):
        try:
            execute_no_yield(self._interpreter.execute_node('_goto'))
        except StatementExit as e:
            self.assertEquals(e.value, '')
        else:
            self.fail("StatementExit not received")
            
    def test_local_function(self):
        try:
            execute_no_yield(self._interpreter.execute_node('local_function'))
        except StatementExit as e:
            self.assertEquals(e.value, '5.67')
        else:
            self.fail("StatementExit not received")
            
    def test_bound_function(self):
        try:
            execute_no_yield(self._interpreter.execute_node('bound_function'))
        except StatementExit as e:
            self.assertEquals(e.value, '2')
        else:
            self.fail("StatementExit not received")
            
    def test_scoped_function(self):
        try:
            execute_no_yield(self._interpreter.execute_node('scoped_function'))
        except StatementExit as e:
            self.assertEquals(e.value, '82')
        else:
            self.fail("StatementExit not received")
            
    def test_local_function_goto(self):
        try:
            execute_no_yield(self._interpreter.execute_node('local_function_goto'))
        except StatementExit as e:
            self.assertEquals(e.value, '')
        else:
            self.fail("StatementExit not received")
            
class ExitTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('nodes_exit')
        
    def test_exit(self):
        try:
            execute_no_yield(self._interpreter.execute_node('n_exit'))
        except StatementExit as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementExit not received")
            
    def test_goto_exit(self):
        try:
            execute_no_yield(self._interpreter.execute_node('goto_exit'))
        except StatementExit as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementExit not received")
            
    def test_function_exit(self):
        try:
            execute_no_yield(self._interpreter.execute_node('function_exit'))
        except StatementExit as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementExit not received")
            
    def test_function_goto_exit(self):
        try:
            execute_no_yield(self._interpreter.execute_node('goto_exit'))
        except StatementExit as e:
            self.assertEquals(e.value, 'test')
        else:
            self.fail("StatementExit not received")
            
