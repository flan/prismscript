"""
tests.functions
=================
Purpose
-------
Offers support for testing the threading interface.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Jan. 24, 2012

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

class ThreadTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('threading')
        
    def test_threading_local(self):
        try:
            execute_no_yield(self._interpreter.execute_function('thread_local', {
             'x': 10,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")

    def test_threading_scoped(self):
        try:
            execute_no_yield(self._interpreter.execute_function('thread_scoped', {
             'x': 10,
            }))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")

class LockTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('locking')
        
    def test_locking(self):
        try:
            execute_no_yield(self._interpreter.execute_function('locking_basic', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")

    def test_locking_thread(self):
        try:
            execute_no_yield(self._interpreter.execute_function('locking_thread', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 50)
        else:
            self.fail("StatementReturn not received")

    def test_locking_thread_cleanup(self):
        try:
            execute_no_yield(self._interpreter.execute_function('locking_thread_cleanup', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")

    def test_locking_nocleanup(self):
        try:
            execute_no_yield(self._interpreter.execute_function('locking_nocleanup', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")

    def test_locking_cleanup(self):
        try:
            execute_no_yield(self._interpreter.execute_function('locking_cleanup', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
