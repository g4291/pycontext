#!/usr/bin/env python3

import threading
import time
import ctypes
import logging
from abc import ABC, abstractmethod
from typing import Type
import time


_logger = logging.getLogger("context")
_ctx_subscribers = dict()


class ContextCancelledError(Exception):
    """ cancel exception """

class ContextTimeoutError(Exception):
    """ cancel exception """

class SubscriberNotUnique(Exception):
    """ subscriber id not unique exception """


def subscribe_context_cancel(id: str, handler: callable):
    if _ctx_subscribers.get(id, None): raise SubscriberNotUnique()
    _ctx_subscribers[id] = handler
    _logger.debug(f"`cancel` subscriber added: {id}, {handler}")

def unsubscribe_context_cancel(id: str):
    if not _ctx_subscribers.get(id, None): return
    del _ctx_subscribers[id]
    _logger.debug(f"`cancel` subscriber removed: {id}")

def cancel_context(id: str):
    handler = _ctx_subscribers.get(id, None)
    if handler: handler()


class AbstractContext(ABC):
    def __init__(self, suppress: bool = False):
        self._thread_id = threading.current_thread().ident
        self._suppress = bool(suppress)

    def _kill(self, error: Type):
        _logger.debug(f"killing thread: {self._thread_id}")
        r = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._thread_id), ctypes.py_object(error))
        if r != 1:
            _logger.error(f"error killing thread, {self._thread_id}")

    @abstractmethod
    def __enter__(self):
        """ abstract """

    @abstractmethod
    def __exit__(self, exc_type, exc_val, traceback):
        """ abstract """


class ContextWithCancel(AbstractContext):
    def __init__(self, id: str, supress: bool = False):
        super().__init__(suppress=supress)

        self._id = id

    def cancel(self):
        self._kill(ContextCancelledError)

    def __enter__(self):
        subscribe_context_cancel(self._id, self.cancel)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        # cleaning
        unsubscribe_context_cancel(self._id)

        # suppress
        if self._suppress and exc_type == ContextCancelledError:
            _logger.info("context cancelled")
            return True

        # log exception
        if exc_type:
            _logger.error(f"context exception, {exc_type}, {exc_val}")


class ContextWithTimeout(AbstractContext):
    def __init__(self, timeout: float, suppress: bool = False):
        super().__init__(suppress)
        self._timeout = float(timeout)
        self._ts = time.time()
        self._running = True
        self._timeout_thread = None

    def _timer(self, timeout: float):

        # timer fn
        def timer():
            while self._running:
                if time.time() > (self._ts + timeout):
                    self._kill(ContextTimeoutError)
                    break

        self._timeout_thread = threading.Thread(target=timer)
        self._timeout_thread.start()

    def __enter__(self):
        if self._timeout > 0:
            self._timer(self._timeout)
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        # cleaning
        self._running = False
        if self._timeout_thread: self._timeout_thread.join()

        # suppress
        if self._suppress and exc_type == ContextTimeoutError:
            _logger.info("context timeout")
            return True

        # log exception
        if exc_type:
            _logger.error(f"context exception, {exc_type}, {exc_val}")


if __name__ == "__main__":
    exit()    