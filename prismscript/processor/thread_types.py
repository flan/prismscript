"""
thread_types
============
Purpose
-------
Provides thread-type-definitions for Prismscript.

Meta
----
:Authors:
    Neil Tallim <flan@uguu.ca>

:Version: Sept. 27, 2012

Legal
-----
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a
letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.
"""
import threading
import time
import types
import warnings

from .errors import (
 StatementExit, StatementReturn,
)
from .grammar.parser import (String)
            
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
        if isinstance(_f, String) or isinstance(_f, types.StringTypes):
            thread_class = _InternalFunctionThread
        else:
            thread_class = _ExternalFunctionThread
        thread = thread_class(self._interpreter, _f, kwargs)
            
        _thread = threading.Thread(target=thread._run)
        _thread.daemon = True
        with self._lock:
            _thread.name = 'prismscript-thread-' + str(self._threads_spawned)
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
    
    def __init__(self, interpreter, function, arguments):
        self._lock = threading.Lock()
        self._pre_running = True
        self._running = False

        self._interpreter = interpreter
        self._function = function
        self._arguments = arguments
        
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
        misbehaving_threads = self._interpreter.release_locks()
        if misbehaving_threads:
            warnings.warn("The following threads did not release locks properly: " + repr(misbehaving_threads))
            
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
        
    def join(self, **kwargs):
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
    def _run_function(self):
        return self._function(**self._arguments)
        
class _InternalFunctionThread(_FunctionThread):
    """
    Executes an interpreter function, 
    """
    def _run_function(self):
        try:
            self._interpreter.execute_function(self._function, self._arguments).send(None)
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
        
    def __call__(self, **kwargs):
        """
        Creates a new supervised lock object.
        """
        lock = _Lock()
        with self._lock:
            self._locks.append(lock)
        return lock

    def release_dead(self, omit_current_thread, **kwargs):
        """
        Iterates over every provisioned lock, releasing all holds made by threads that no longer
        exist. If `omit_current_thread` is set, the current thread is considered dead.

        A list of all offending threads is returned.
        """
        bad_threads = []
        with self._lock:
            for lock in self._locks:
                bad_thread = lock.release_dead(omit_current_thread)
                if bad_thread:
                    bad_threads.append(bad_thread)
        return bad_threads
        
class _Lock:
    """
    A wrapper around a re-entrant lock, adding support for supervised thread-management.
    """
    def __init__(self):
        self._lock = threading.RLock() #A lock to control access to the acquisition history. A lock with a lock.
        self._locker = None
        self._lock_count = 0
        self._rlock = threading.RLock()

    @property
    def acquired(self):
        """
        Indicates whether the lock is currently in a locked state.
        """
        return bool(self._locker)

    def release_dead(self, omit_current_thread, **kwargs):
        """
        Iterates over every existing thread, releasing all holds on this lock if the locker has
        died. If `omit_current_thread` is set, the current thread is considered dead.

        If the lock is released, the thread's instance is returned.
        """
        with self._lock:
            if self._locker and ((omit_current_thread and self._locker == threading.current_thread()) or not self._locker in threading.enumerate()):
                locker = self._locker
                while self._lock_count:
                    self.release()
                return self._locker
                
    def acquire(self, **kwargs):
        """
        Acquires the underlying lock and tracks the locker.
        """
        self._rlock.acquire()
        with self._lock:
            if not self._lock_count:
                self._locker = threading.current_thread()
            self._lock_count += 1
            
    def release(self, **kwargs):
        """
        Releases the underlying lock and stops tracking the locker, if not nested.
        """
        self._rlock.release()
        with self._lock:
            self._lock_count -= 1
            if not self._lock_count:
                self._locker = None

    locked = acquired
    lock = acquire
    unlock = release
    
