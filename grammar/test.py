#!/usr/bin/env python
"""
test
====
Purpose
-------
Provides an entry-point for running unit tests over the language's grammar. Invoking this every time
you make a change, no matter how slight, is a very, very good idea.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: 1.0.0 : Oct. 17, 2010

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""

"""
Unlike most things that need to be tested, the best way to trace errors in this project is to use
exceptions to identify inconsistencies. For this reason, all tests are either expecting a None
return or an exception. Just something to keep in mind while reading.
"""
import unittest

import parser

import tests.primitive
import tests.structure
import tests.expressions

if __name__ == '__main__':
    all_tests = unittest.TestSuite((
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(tests.primitive.NodeTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.primitive.FunctionTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.primitive.NamespaceTestCase),
     )),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(tests.expressions.CommentsTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.expressions.TermsTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.expressions.MathsTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.expressions.TestsTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.expressions.SequencesTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.expressions.StatementsTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.expressions.AssignmentsTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.expressions.FunctionCallsTestCase),
     )),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(tests.structure.ExpressionListTestCase),
      unittest.TestLoader().loadTestsFromTestCase(tests.structure.ConditionalTestCase),
     )),
    ))
    unittest.TextTestRunner().run(all_tests)
    
