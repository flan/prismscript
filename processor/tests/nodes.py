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
)

class SimpleTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('nodes')
        
    def test_simple(self):
        self.assertIsNone(self._interpreter.execute_node('simple'))
        
    def test_goto(self):
        self.assertIsNone(self._interpreter.execute_node('goto'))
        
    def test_local_function(self):
        self.assertIsNone(self._interpreter.execute_node('local_function'))
        
    def test_scoped_function(self):
        self.assertIsNone(self._interpreter.execute_node('scoped_function'))
        
    def test_local_function_goto(self):
        self.assertIsNone(self._interpreter.execute_node('local_function_goto'))
        
