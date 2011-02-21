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

class ScopesTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('expressions')
        try:
            execute_no_yield(self._interpreter.execute_node('setup_scopes'))
        except StatementExit: #Expected
            pass
        else:
            self.fail("StatementExit not received")
            
    def test_local_auto(self):
        try:
            execute_no_yield(self._interpreter.execute_function('local_auto', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_local_auto2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('local_auto2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 4)
        else:
            self.fail("StatementReturn not received")
            
    def test_local_local(self):
        try:
            execute_no_yield(self._interpreter.execute_function('local_local', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 4)
        else:
            self.fail("StatementReturn not received")
            
    def test_local_global(self):
        try:
            execute_no_yield(self._interpreter.execute_function('local_global', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_local_global2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('local_global', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_scoped_local_auto(self):
        try:
            execute_no_yield(self._interpreter.execute_function('scoped_local_auto', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 3)
        else:
            self.fail("StatementReturn not received")
            
    def test_scoped_local_auto2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('scoped_local_auto2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 2)
        else:
            self.fail("StatementReturn not received")
            
class TypesTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('expressions')
        
    def test_bool(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_string(self):
        try:
            execute_no_yield(self._interpreter.execute_function('string', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, "hello")
        else:
            self.fail("StatementReturn not received")
            
    def test_integer(self):
        try:
            execute_no_yield(self._interpreter.execute_function('integer', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, -5134)
        else:
            self.fail("StatementReturn not received")
            
    def test_float(self):
        try:
            execute_no_yield(self._interpreter.execute_function('float', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 6.23)
        else:
            self.fail("StatementReturn not received")
            
    def test_none(self):
        try:
            execute_no_yield(self._interpreter.execute_function('none', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, None)
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 'b', 3.45))
        else:
            self.fail("StatementReturn not received")
            
class TestsTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('expressions')
        
    def test_equality(self):
        try:
            execute_no_yield(self._interpreter.execute_function('equality', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_equality2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('equality2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_inequality(self):
        try:
            execute_no_yield(self._interpreter.execute_function('inequality', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_inequality2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('inequality2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_greater_equal(self):
        try:
            execute_no_yield(self._interpreter.execute_function('greater_equal', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_greater_equal2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('greater_equal2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_greater(self):
        try:
            execute_no_yield(self._interpreter.execute_function('greater', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_greater2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('greater2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_lesser_equal(self):
        try:
            execute_no_yield(self._interpreter.execute_function('lesser_equal', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_lesser_equal2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('lesser_equal2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_lesser(self):
        try:
            execute_no_yield(self._interpreter.execute_function('lesser', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_lesser2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('lesser2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool_or(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool_or', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool_or2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool_or2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool_or3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool_or3', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool_or4(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool_or4', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool_and(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool_and', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool_and2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool_and2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool_and3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool_and3', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool_and4(self):
        try:
            execute_no_yield(self._interpreter.execute_function('bool_and4', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
