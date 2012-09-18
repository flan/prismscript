"""
tests.expressions
=================
Purpose
-------
Offers support for testing expressions.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Sept. 18, 2011

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
from ..local_types import (Dictionary, Set, Sequence)

class _BaseTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('types')
        
class MarshallingTestCase(_BaseTestCase):
    def _test(self, value):
        try:
            execute_no_yield(self._interpreter.execute_function('convert', {'v': value}))
        except StatementReturn as e:
            self.assertEquals(e.value, value)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool_true(self):
        self._test(True)
        
    def test_bool_false(self):
        self._test(False)
        
    def test_float(self):
        self._test(7.67)
        
    def test_int(self):
        self._test(5)
        
    def test_string(self):
        self._test('Hello, world!')
        
    def test_none(self):
        self._test(None)
        
    def test_list(self):
        self._test([1, 2, 3])
        
    def test_dict(self):
        self._test({1: 2, 'a': 'b', 5.0: 4.3})
        
    def test_set(self):
        self._test(set([1, 'a', 5.0]))
        
class RecursionTestCase(_BaseTestCase):
    def test_list(self):
        value = [1, [2, 3]]
        try:
            execute_no_yield(self._interpreter.execute_function('convert', {'v': value}))
        except StatementReturn as e:
            self.assertEquals(e.value, value)
            self.assertTrue(isinstance(e.value, Sequence))
            self.assertTrue(isinstance(e.value[1], Sequence))
        else:
            self.fail("StatementReturn not received")
            
    def test_dict(self):
        value = {'a': 1, 'c': {2: 'b'}}
        try:
            execute_no_yield(self._interpreter.execute_function('convert', {'v': value}))
        except StatementReturn as e:
            self.assertEquals(e.value, value)
            self.assertTrue(isinstance(e.value, Dictionary))
            self.assertTrue(isinstance(e.value.get('c'), Dictionary))
        else:
            self.fail("StatementReturn not received")
            
