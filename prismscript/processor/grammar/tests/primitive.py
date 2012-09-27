"""
tests.primitive
===============
Purpose
-------
Offers the most primitive battery of tests for the language, ensuring that nodes and functions can
be declared and referenced and that they can hold expression-lists.

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
import unittest

from .. import parser
from . import _GenericTestCase

class FunctionTestCase(_GenericTestCase):
    def test_function(self):
        self._test('function')

    def test_function_broken(self):
        self._test_error('function_broken', False)
        
    def test_function_broken_2(self):
        self._test_error('function_broken_2', False)
        
    def test_function_expressions(self):
        self._test('function_expressions')
        

class NamespaceTestCase(_GenericTestCase):
    def test_namespace(self):
        self._test('namespace')
        
    def test_namespace_broken_function(self):
        self._test_error('namespace_broken_function', False)
        
    def test_namespace_broken_function_signature(self):
        self._test_error('namespace_broken_function_signature', False)
        
    def test_namespace_broken_node(self):
        self._test_error('namespace_broken_node', True)

class NodeTestCase(_GenericTestCase):
    def test_node(self):
        self._test('node')

    def test_node_broken(self):
        self._test_error('node_broken', True)
        
    def test_node_expressions(self):
        self._test('node_expressions')
        
