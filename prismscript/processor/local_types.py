"""
types
=====
Purpose
-------
Provides core type-definitions for Prismscript.

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
import random
import threading
import time
import types

from .errors import (
 StatementExit, StatementReturn,
)

def convert_bool(v, **kwargs):
    return bool(v)
    
def convert_float(v, **kwargs):
    try:
        return float(v)
    except Exception:
        return None
        
def convert_int(v, base=None, is_char=False, **kwargs):
    try:
        if base:
            return int(v, base)
        elif is_char:
            return ord(v)
        else:
            return int(v)
    except Exception:
        return None
        
def convert_string(v, int_base=None, is_char=False, **kwargs):
    if int_base:
        if not 2 <= int_base <= 36:
            raise ValueError("Integer base must be between 2 and 36, inclusive, not %(i)r" % {
             'i': int_base,
            })
        if not type(v) == int:
            raise ValueError("Unable to process non-integer value %(i)r" % {
             'i': v,
            })
        num_base = 48 #Ascii 0
        asc_offset = 39 #Distance from 0 to 'a'.
        output = []
        while v:
            v_mod = v % int_base
            v //= int_base
            output.insert(0, chr(num_base + v_mod + (v_mod > 10 and asc_offset or 0)))
        return ''.join(output)
    elif is_char:
        return chr(v)
    else:
        return str(v)
        
class _Container:
    """
    A generic data-type for any structure that has a variable length.
    """
    def copy(self, **kwargs):
        return self.__class__(self)
        
    def contains(self, item, **kwargs):
        return item in self
        
    def _get_size(self):
        return len(self)
    length = property(_get_size)
    
class Dictionary(dict, _Container):
    """
    A Prismscript-friendly wrapper around a dictionary.
    
    Objects of this type may be passed to any Python function that expects a dict.
    """
    def __init__(self, items=[], **kwargs):
        dict.__init__(self, items)
        
    def get(self, key, default=None, **kwargs):
        return dict.get(self, key, default)
        
    def put(self, key, value, **kwargs):
        self[key] = value
        
    def remove(self, key, **kwargs):
        if key in self:
            del self[key]
            
    def get_items(self, **kwargs):
        items = Sequence()
        for item in self.items():
            items.append(Sequence(item))
        return items
        
    def get_keys(self, **kwargs):
        return Sequence(self.keys())
        
    def get_values(self, **kwargs):
        return Sequence(self.values())
        
class Set(set, _Container):
    """
    A Prismscript-friendly wrapper around a set.
    
    Objects of this type may be passed to any Python function that expects a set.
    """
    def __init__(self, items=[], **kwargs):
        set.__init__(self, items)
        
    def add(self, item, **kwargs):
        set.add(self, item)
        
    def remove(self, item, **kwargs):
        set.discard(self, item)
        
    def get_items(self, **kwargs):
        return Sequence(self)
        
    def difference(self, other_set, **kwargs):
        return Set(set.difference(self, other_set))
        
    def intersection(self, other_set, **kwargs):
        return Set(set.intersection(self, other_set))
        
    def union(self, other_set, **kwargs):
        return Set(set.union(self, other_set))
        
class Sequence(list, _Container):
    """
    A Prismscript-friendly wrapper around a list.
    
    Objects of this type may be passed to any Python function that expects a sequence.
    """
    def __init__(self, items=[], **kwargs):
        list.__init__(self, items)
        
    def append(self, item, **kwargs):
        list.append(self, item, **kwargs)
        
    def prepend(self, item, **kwargs):
        self.insert(0, item)
        
    def get(self, index, **kwargs):
        return self[index]
        
    def insert(self, index, item, **kwargs):
        list.insert(self, index, item)
        
    def remove(self, index, **kwargs):
        del self[index]
        
    def pop_head(self, **kwargs):
        return self.pop(0)
        
    def pop_item(self, index, **kwargs):
        return self.pop(index)
        
    def pop_tail(self, **kwargs):
        return self.pop()
        
    def reverse(self, **kwargs):
        list.reverse(self)
        
    def shuffle(self, **kwargs):
        random.shuffle(self)
        
    def sort(self, **kwargs):
        list.sort(self)
        
    def slice(self, start=None, end=None, **kwargs):
        if not start is None and not end is None:
            return self[start:end]
        elif not start is None:
            return self[start:]
        elif not end is None:
            return self[:end]
        else:
            return self.copy()

            
class ThreadFactory:
    """
    A thread-factory that spawns the correct thread-instance for the given function.
    """
    def __init__(self, interpreter):
        self._interpreter = interpreter
        self._lock = threading.Lock()
        self._threads_spawned = 0
        
    def __call__(self, _f, **kwargs):
        """
        Creates and runs a thread instance when an instance of this object-type is invoked,
        permitting transparent pass-through of the interpreter instance.
        
        `_f` may be either a string, for a prismscript function, or a Python callable. All other
        arguments are passed to `_f` when it is invoked. The returned value is the instantiated
        thread.
        """
        if type(_f) in types.StringTypes:
            thread = _InternalFunctionThread(self._interpreter, _f, kwargs)
        else:
            thread = _ExternalFunctionThread(_f, kwargs)
            
        _thread = threading.Thread(target=thread._run)
        _thread.daemon = True
        with self._lock:
            _thread.name = = 'prismscript-thread-' + str(self._threads_spawned)
            self._threads_spawned += 1
        _thread.start()
        return thread
        
class _FunctionThread:
    """
    A wrapper for a function that executes in a thread, collecting its output for deferred
    retrieval.
    """
    _result = None
    _exception = False
    
    def __init__(self):
        self._lock = threading.Lock()
        self._pre_running = True
        self._running = False
        
    def _run(self):
        """
        Handles execution of the thread's task.
        """
        with self._lock:
            self._running = True
            self._pre_running = False
            try:
                self._result = self._run_function()
            except Exception as e:
                self._result = e
                self._exception = True
            self._running = False
            
    @property
    def exception(self):
        """
        If the thread's task completed with an exception, this will be ``True``. The exception
        itself is available as the thread's ``result``.
        """
        return self._exception
        
    @property
    def result(self):
        """
        Provides the result of the thread's task; this is an exception instance if ``exception``
        is ``True``.
        
        The value contained here is meaningful only after the thread has finished running.
        """
        return self._result
        
    @property
    def running(self):
        """
        Can be used to check to see whether the thread is still running; useful in case a decision
        needs to be made about performing another parallel task, but not usually as convenient as
        ``join()``.
        
        A thread is considered running from the moment it is created until its task has completed.
        """
        return self._running or self._pre_running
        
    def join(self):
        """
        Blocks until the thread has finished executing; should be invoked prior to checking the
        result.
        """
        while self._pre_running:
            time.sleep(0.05)
        self._lock.acquire()
        self._lock.release()
        
class _ExternalFunctionThread(_FunctionThread):
    """
    Executes a Python function.
    """
    def __init__(self, function, arguments):
        self._function = function
        self._arguments = arguments
        
    def _run_function(self):
        return self._function(**self._arguments)
        
class _InternalFunctionThread(_FunctionThread):
    """
    Executes an interpreter function, 
    """
    def __init__(self, interpreter, function, arguments):
        self._interpreter = interpreter
        self._function = function
        self._arguments = arguments
        
    def _run_function(self):
        try:
            self._interpreter.execute_function(self._function, self._arguments)
        except (StatementExit, StatementReturn) as e:
            return e.value
        raise ValueError("Indicated function did not return a value; most likely cause: an occurrence of the co-routine interface was encountered")
        
class LockFactory:
    """
    A lock-factory that spawns lock objects that automatically unlock when their holding thread
    terminates unexpectedly.
    """
    def __init__(self, interpreter):
        self._interpreter = interpreter
        self._lock = threading.Lock()
        self._locks = []
        
    def __call__(self):
        """
        Creates a new supervised lock object.
        """
        lock = _Lock()
        with self._lock:
            self._locks.append(lock)
        return lock

    def release_dead(self):
        with self._lock:
            for lock in self._locks:
                lock.release_dead()
                
class _Lock:
    """
    A wrapper around a re-entrant lock, adding support for supervised thread-management.
    """
    def __init__(self):
        self._lock = threading.RLock() #A lock to control access to the acquisition history. A lock with a lock.
        self._locker = None
        self._lock_count = 0
        self._rlock = threading.RLock()

    def release_dead(self):
        with self._lock:
            if self._locker and not self._locker in threading.enumerate():
                while self._lock_count:
                    self.release()
                    
    def acquire(self):
        self._rlock.acquire()
        with self._lock:
            if not self._lock_count:
                self._locker = threading.current_thread()
            self._lock_count += 1
            
    def release(self):
        self._rlock.release()
        with self._lock:
            self._lock_count -= 1
            if not self._lock_count:
                self._locker = None
                
