import logging
import sys
from contextlib import contextmanager
from functools import wraps
from typing import NoReturn, Union, TextIO, Optional, Callable

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
    num_context_lines: int = 1,
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
                num_context_lines=num_context_lines,
            ):
                file_.write(trace_str + '\n')

            if flush:
                file_.flush()

        if reraise:
            raise e


def prints_tb(
    func__for_noncall_case_only: Optional[Callable] = None,  # to call without "()"
    file_: Optional[Union[TextIO, LoggerAsFile]] = sys.stderr,
    flush: bool = False,
    num_context_lines: int = 1,
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
):
    if func__for_noncall_case_only:
        return prints_tb(
            file_=file_,
            flush=flush,
            num_context_lines=num_context_lines,
            max_value_str_len=max_value_str_len,
            max_exc_str_len=max_exc_str_len,
            ellipsis_=ellipsis_,
        )(func__for_noncall_case_only)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with printing_tb(
                reraise=True,
                file_=file_,
                flush=flush,
                skip_cur_frame=True,
                num_context_lines=num_context_lines,
                max_value_str_len=max_value_str_len,
                max_exc_str_len=max_exc_str_len,
                ellipsis_=ellipsis_,
            ):
                return func(*args, **kwargs)

        return wrapper

    return decorator
