import inspect
import logging
import sys
from contextlib import contextmanager
from functools import wraps
from typing import NoReturn, Union, TextIO, Optional

from traceback_with_variables.core import iter_tb_lines


class LoggerAsFile:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def flush(self) -> NoReturn:
        pass

    def write(self, text: str) -> NoReturn:
        for line in text.rstrip('\r\n').split('\n'):
            self.logger.error(line)


@contextmanager
def printing_tb(
    reraise: bool = True,
    file_: Optional[Union[TextIO, LoggerAsFile]] = sys.stderr,
    flush: bool = False,
    skip_cur_frame: bool = False,
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
):
    try:
        yield

    except Exception as e:
        if file_:
            for trace_str in iter_tb_lines(
                e=e,
                tb=None,
                num_skipped_frames=2 if skip_cur_frame else 1,
                max_value_str_len=max_value_str_len,
                max_exc_str_len=max_exc_str_len,
                ellipsis_=ellipsis_,
            ):
                file_.write(trace_str + '\n')

            if flush:
                file_.flush()

        if reraise:
            raise e


def prints_tb(
    file_: Union[TextIO, LoggerAsFile] = sys.stderr,
    flush: bool = False,
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with printing_tb(
                reraise=True,
                file_=file_,
                flush=flush,
                skip_cur_frame=True,
                max_value_str_len=max_value_str_len,
                max_exc_str_len=max_exc_str_len,
                ellipsis_=ellipsis_,
            ):
                return func(*args, **kwargs)

        return wrapper

    return decorator
