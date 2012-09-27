#!/usr/bin/env python
"""
test
====
Purpose
-------
Provides an entry-point for running unit tests over the language's interpreter. Invoking this every
time you make a change, no matter how slight, is a very, very good idea.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Feb. 19, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import unittest

from processor.tests import expressions
from processor.tests import nodes
from processor.tests import functions
from processor.tests import conditionals
from processor.tests import complex
from processor.tests import threading
from processor.tests import types

if __name__ == '__main__':
    all_tests = unittest.TestSuite((
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(types.MarshallingTestCase),
      unittest.TestLoader().loadTestsFromTestCase(types.RecursionTestCase),
     )),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(expressions.ScopesTestCase),
      unittest.TestLoader().loadTestsFromTestCase(expressions.TypesTestCase),
      unittest.TestLoader().loadTestsFromTestCase(expressions.ConversionTestCase),
      unittest.TestLoader().loadTestsFromTestCase(expressions.SequenceTestCase),
      unittest.TestLoader().loadTestsFromTestCase(expressions.SetTestCase),
      unittest.TestLoader().loadTestsFromTestCase(expressions.DictionaryTestCase),
      unittest.TestLoader().loadTestsFromTestCase(expressions.TestsTestCase),
      unittest.TestLoader().loadTestsFromTestCase(expressions.SuffixesTestCase),
     )),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(nodes.SimpleTestCase),
      unittest.TestLoader().loadTestsFromTestCase(nodes.ExitTestCase),
     )),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(functions.MathTestCase),
     )),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(conditionals.IfTestCase),
      unittest.TestLoader().loadTestsFromTestCase(conditionals.WhileTestCase),
      unittest.TestLoader().loadTestsFromTestCase(conditionals.ForTestCase),
     )),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(complex.NestedTestCase),
      unittest.TestLoader().loadTestsFromTestCase(complex.CoroutineTestCase),
     )),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(threading.ThreadTestCase),
      unittest.TestLoader().loadTestsFromTestCase(threading.LockTestCase),
     )),
    ))
    unittest.TextTestRunner().run(all_tests)
    

