"""
stdlib.lang
===========
Purpose
-------
Provides core language features for Prismscript.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: Feb. 20, 2011

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
try:
    from prismscript.processor.local_types import Sequence
except ImportError:
    from processor.local_types import Sequence

from . import convert
from . import string

_zip = zip

def build_range(stop, start=0, step=1, **kwargs):
    return range(start, stop, step)

def zip(sequences, pad=False, pad_values=None, **kwargs):
    if pad and pad_values:
        sequences = [list(s) for s in sequences]
        sequence_length = max([len(s) for s in sequences])
        for (sequence, padding) in zip(sequences, pad_values):
            sequence += [padding] * (sequence_length - len(sequence))
    return Sequence([Sequence(s) for s in _zip(*sequences)])
    
