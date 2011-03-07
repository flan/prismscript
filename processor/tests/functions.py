"""
tests.functions
=================
Purpose
-------
Offers support for testing interpreted functions directly.

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

class MathTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('math')
        
    def test_add_str(self):
        try:
            execute_no_yield(self._interpreter.execute_function('add', {
             'x': 'eggs',
             'y': 'spam',
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 'eggsspam')
        else:
            self.fail("StatementReturn not received")
            
    def test_add_str_int(self):
        try:
            execute_no_yield(self._interpreter.execute_function('add', {
             'x': 'eggs',
             'y': 5,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 'eggs5')
        else:
            self.fail("StatementReturn not received")
            
    def test_add_int_str(self):
        try:
            execute_no_yield(self._interpreter.execute_function('add', {
             'x': 5,
             'y': 'spam',
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, '5spam')
        else:
            self.fail("StatementReturn not received")
            
    def test_add_sequence(self):
        try:
            execute_no_yield(self._interpreter.execute_function('add', {
             'x': [1, 2, 3],
             'y': [4, 5, 6],
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, [1, 2, 3, 4, 5, 6])
        else:
            self.fail("StatementReturn not received")
            
    def test_add(self):
        try:
            execute_no_yield(self._interpreter.execute_function('add', {
             'x': 2,
             'y': 3,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_subtract(self):
        try:
            execute_no_yield(self._interpreter.execute_function('subtract', {
             'x': 2,
             'y': 3,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, -1)
        else:
            self.fail("StatementReturn not received")
            
    def test_multiply(self):
        try:
            execute_no_yield(self._interpreter.execute_function('multiply', {
             'x': 2,
             'y': 3,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 6)
        else:
            self.fail("StatementReturn not received")
            
    def test_divide(self):
        try:
            execute_no_yield(self._interpreter.execute_function('divide', {
             'x': 3,
             'y': 2,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 1.5)
        else:
            self.fail("StatementReturn not received")
            
    def test_int_divide(self):
        try:
            execute_no_yield(self._interpreter.execute_function('int_divide', {
             'x': 3,
             'y': 2,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_mod(self):
        try:
            execute_no_yield(self._interpreter.execute_function('mod', {
             'x': 3,
             'y': 2,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_mod2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('mod', {
             'x': 3.5,
             'y': 1.25,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 1.0)
        else:
            self.fail("StatementReturn not received")
            
    def test_exponentiate(self):
        try:
            execute_no_yield(self._interpreter.execute_function('exponentiate', {
             'x': 2,
             'y': 3,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 8)
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_add_str(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_add', {
             'x': 'eggs',
             'y': 'spam',
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 'eggsspam')
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_add_str_int(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_add', {
             'x': 'eggs',
             'y': 5,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 'eggs5')
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_add_int_str(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_add', {
             'x': 5,
             'y': 'spam',
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, '5spam')
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_add_sequence(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_add', {
             'x': [1, 2, 3],
             'y': [4, 5, 6],
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, [1, 2, 3, 4, 5, 6])
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_add(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_add', {
             'x': 2,
             'y': 3,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_subtract(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_subtract', {
             'x': 2,
             'y': 3,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, -1)
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_multiply(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_multiply', {
             'x': 2,
             'y': 3,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 6)
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_divide(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_divide', {
             'x': 3,
             'y': 2,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 1.5)
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_int_divide(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_int_divide', {
             'x': 3,
             'y': 2,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_mod(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_mod', {
             'x': 3,
             'y': 2,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_assign_mod2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('assign_mod', {
             'x': 3.5,
             'y': 1.25,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 1.0)
        else:
            self.fail("StatementReturn not received")
            
