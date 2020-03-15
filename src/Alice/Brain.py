import logging
import sys
import time
import traceback
from functools import partial
LOG = logging.getLogger(__name__)


class TimeEstimate:
    def __init__(self, block_name="", without_any_args=False, handler=None):
        self._block_name = block_name
        self._without_any_args = without_any_args
        self._handler = handler
        self._time_list = [0.0, 0.0]

    def __call__(self, func):
        self._func = func
        if not bool(self._block_name) and self._func is not None:
            self._block_name = self._func.__name__
        if self._handler is None:
            self._handler = partial(print, "time of {}:".format(self._block_name))

        def wrapper(*args, **kwargs):
            LOG.debug("args: {}, kwargs: {}".format(args, kwargs))
            self._time_list[0] = time.perf_counter()
            if not self._without_any_args:
                result = self._func(*args, **kwargs)
            else:
                result = self._func()
            self._time_list[1] = time.perf_counter()
            time_diff = self._time_list[1] - self._time_list[0]
            LOG.debug("time of {}: {}".format(self._block_name, time_diff))
            self._handler(time_diff)
            return result

        return wrapper

    def __enter__(self):
        if self._handler is None:
            self._handler = partial(print, "time of {}:".format(self._block_name))
        self._time_list[0] = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._time_list[1] = time.perf_counter()
        time_diff = self._time_list[1] - self._time_list[0]
        LOG.debug("time of {}: {}".format(self._block_name, time_diff))
        self._handler(time_diff)


class ExceptionCatch:
    def __init__(self, handler=partial(print, file=sys.stderr)):
        self._handler = handler
        sys.excepthook = self.__call__
        LOG.debug("exception hook to handler")

    def __call__(self, etype, value, tb):
        msg = "".join(traceback.format_exception(etype, value, tb))
        self._handler(msg)


class ThreadObject:
    def __init__(self):
        pass
