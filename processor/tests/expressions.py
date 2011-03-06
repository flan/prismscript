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

class ConversionTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('expressions')
        
    def test_bool(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_bool', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
    def test_bool2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_bool2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_float(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_float', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5.65)
        else:
            self.fail("StatementReturn not received")
            
    def test_float2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_float2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, -5.65)
        else:
            self.fail("StatementReturn not received")

    def test_float3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_float3', {}))
        except StatementReturn as e:
            self.assertIsNone(e.value)
        else:
            self.fail("StatementReturn not received")

    def test_integer(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_integer', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")
            
    def test_integer2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_integer2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, -5)
        else:
            self.fail("StatementReturn not received")

    def test_integer3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_integer3', {}))
        except StatementReturn as e:
            self.assertIsNone(e.value)
        else:
            self.fail("StatementReturn not received")
            
    def test_string(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_string', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 'True')
        else:
            self.fail("StatementReturn not received")

    def test_string2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_string2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, '-65')
        else:
            self.fail("StatementReturn not received")

    def test_string3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_string3', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, '5.65')
        else:
            self.fail("StatementReturn not received")

    def test_string4(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_string4', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 'None')
        else:
            self.fail("StatementReturn not received")

    def test_string5(self):
        try:
            execute_no_yield(self._interpreter.execute_function('convert_string5', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 'whee')
        else:
            self.fail("StatementReturn not received")
            
class SequenceTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('expressions')
        
    def test_sequence(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 'b', 3.45))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence2', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 'b', 3.45))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence3', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 'b', 3.45))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_append(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_append', {'v': 3}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 2, 3))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_copy(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_copy', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value[1], (1, 2, 3))
            self.assertSequenceEqual(e.value[0], (1, 2, 3, 4))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_contains(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_contains', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True )
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_contains2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_contains2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_get(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_get', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 2)
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_insert(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_insert', {'v': 2}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 2, 3))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_length(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_length', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 3)
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_pop_head(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_pop_head', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value[1], (2, 3))
            self.assertEquals(e.value[0], 1)
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_pop_item(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_pop_item', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value[1], (1, 3))
            self.assertEquals(e.value[0], 2)
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_pop_tail(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_pop_tail', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value[1], (1, 2))
            self.assertEquals(e.value[0], 3)
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_prepend(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_prepend', {'v': 1}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 2, 3))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_remove(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_remove', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 3))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_reverse(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_reverse', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 2, 3))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_shuffle(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_shuffle', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(sorted(e.value), (1, 2, 3))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_slice(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_slice', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (2,))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_slice2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_slice2', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (2, 3))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_slice3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_slice3', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 2))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_slice4(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_slice4', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 2, 3))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_sort(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_sort', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 2, 3))
        else:
            self.fail("StatementReturn not received")
            
    def test_sequence_assign(self):
        try:
            execute_no_yield(self._interpreter.execute_function('sequence_assign', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1, 2, 4))
        else:
            self.fail("StatementReturn not received")
            
class DictionaryTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('expressions')
        
    def test_dictionary(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary', {}))
        except StatementReturn as e:
            self.assertDictEqual(e.value, {1: 2})
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary2', {}))
        except StatementReturn as e:
            self.assertDictEqual(e.value, {1: 2})
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary3', {}))
        except StatementReturn as e:
            self.assertDictEqual(e.value, {1: 2})
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_contains(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_contains', {}))
        except StatementReturn as e:
            self.assertTrue(e.value)
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_contains2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_contains2', {}))
        except StatementReturn as e:
            self.assertFalse(e.value)
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_copy(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_copy', {}))
        except StatementReturn as e:
            self.assertDictEqual(e.value[0], {1: 2})
            self.assertDictEqual(e.value[1], {1: 2, 3:4})
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_get(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_get', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 2)
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_get2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_get2', {}))
        except StatementReturn as e:
            self.assertIsNone(e.value)
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_get3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_get3', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 5)
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_get_items(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_get_items', {}))
        except StatementReturn as e:
            self.assertEquals(len(e.value), 1)
            self.assertSequenceEqual(e.value[0], (1, 2))
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_get_keys(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_get_keys', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1,))
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_get_values(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_get_values', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (2,))
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_length(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_length', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, 2)
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_put(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_put', {}))
        except StatementReturn as e:
            self.assertDictEqual(e.value, {1: 2})
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_remove(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_remove', {}))
        except StatementReturn as e:
            self.assertDictEqual(e.value, {})
        else:
            self.fail("StatementReturn not received")  
            
    def test_dictionary_remove2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('dictionary_remove2', {}))
        except StatementReturn as e:
            self.assertDictEqual(e.value, {1: 2})
        else:
            self.fail("StatementReturn not received")  
            
class SetTestCase(unittest.TestCase):
    _interpreter = None
    
    def setUp(self):
        self._interpreter = get_interpreter('expressions')
        
    def test_set(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set([1]))
        else:
            self.fail("StatementReturn not received")
            
    def test_set2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set2', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set([1]))
        else:
            self.fail("StatementReturn not received")
            
    def test_set3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set3', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set([1]))
        else:
            self.fail("StatementReturn not received")
            
    def test_set_add(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_add', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set([1]))
        else:
            self.fail("StatementReturn not received")
            
    def test_set_add2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_add2', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set([1]))
        else:
            self.fail("StatementReturn not received")
            
    def test_set_contains(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_contains', {}))
        except StatementReturn as e:
            self.assertTrue(e.value)
        else:
            self.fail("StatementReturn not received")
            
    def test_set_contains2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_contains2', {}))
        except StatementReturn as e:
            self.assertFalse(e.value)
        else:
            self.fail("StatementReturn not received")
            
    def test_set_copy(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_copy', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value[0], set([1]))
            self.assertSetEqual(e.value[1], set([1, 2]))
        else:
            self.fail("StatementReturn not received")
            
    def test_set_difference(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_difference', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set([1]))
        else:
            self.fail("StatementReturn not received")
            
    def test_set_get_items(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_get_items', {}))
        except StatementReturn as e:
            self.assertSequenceEqual(e.value, (1,))
        else:
            self.fail("StatementReturn not received")
            
    def test_set_intersection(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_intersection', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set([2]))
        else:
            self.fail("StatementReturn not received")
            
    def test_set_remove(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_remove', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set())
        else:
            self.fail("StatementReturn not received")
            
    def test_set_remove2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_remove2', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set([1]))
        else:
            self.fail("StatementReturn not received")
            
    def test_set_union(self):
        try:
            execute_no_yield(self._interpreter.execute_function('set_union', {}))
        except StatementReturn as e:
            self.assertSetEqual(e.value, set([1, 2, 3]))
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
            
    def test_not(self):
        try:
            execute_no_yield(self._interpreter.execute_function('not', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")

    def test_not2(self):
        try:
            execute_no_yield(self._interpreter.execute_function('not2', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, False)
        else:
            self.fail("StatementReturn not received")

    def test_not3(self):
        try:
            execute_no_yield(self._interpreter.execute_function('not3', {}))
        except StatementReturn as e:
            self.assertEquals(e.value, True)
        else:
            self.fail("StatementReturn not received")
            
