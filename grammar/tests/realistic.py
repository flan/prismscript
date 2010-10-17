"""
tests.realistic
===============
Purpose
-------
Offers unit tests that either reflect or approximate real-world deployments of the language.

Whenever a particularly novel or complex script is written, it should be added as a test in this
module, to ensure that future updates to the language don't stop anything from working.

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

from . import parser
from . import (
 get_source, get_digest, compare_nodesets,
)

class TheoreticalTestCase(unittest.TestCase):
    def test_io_model(self):
        source = get_source('theoretical_io_model')
        (nodes, functions) = get_digest('theoretical_io_model')

        (digest_nodes, digest_functions, digest) = parser.parse(source)

        self.assertEquals(compare_nodesets(nodes, digest_nodes), None)
        
