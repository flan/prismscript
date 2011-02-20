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

from processor.tests import nodes
from processor.tests import functions
from processor.tests import complex

if __name__ == '__main__':
    all_tests = unittest.TestSuite((
     #unittest.TestSuite((
     # unittest.TestLoader().loadTestsFromTestCase(nodes.SimpleTestCase),
     # unittest.TestLoader().loadTestsFromTestCase(nodes.ReferenceTestCase),
     #)),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(functions.MathTestCase),
     )),
     unittest.TestSuite((
      unittest.TestLoader().loadTestsFromTestCase(complex.NestedTestCase),
     ))
    ))
    unittest.TextTestRunner().run(all_tests)
    
"""
import prismscript.interpreter
i = prismscript.interpreter.Interpreter(open('quickcall.src').read())
print(i.list_nodes())
print(i.list_functions())

print()

i.execute_node('setup')

print()

print(i._globals)
for l in i.get_log():
    print('\t' + l)
"""

