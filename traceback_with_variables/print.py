import logging
import sys
from contextlib import contextmanager
from functools import wraps
from typing import NoReturn, Union, TextIO, Optional, Callable

from traceback_with_variables.color import choose_color_scheme
from traceback_with_variables.core import iter_tb_lines, ColorScheme, ColorSchemes


class LoggerAsFile:
    def __init__(self, logger: logging.Logger, separate_lines: bool = False):
        self.logger = logger
        self.separate_lines = separate_lines
        self.lines = []

    def flush(self) -> NoReturn:
        if self.lines:
            self.logger.error('\n    '.join(self.lines))

    def write(self, text: str) -> NoReturn:
        if not text.strip('\n'):
            return

        if self.separate_lines:
            for line in text.rstrip().split('\n'):
                self.logger.error(line)
        else:
            self.lines.append(text)


@contextmanager
def printing_tb(
    reraise: bool = True,
    file_: Optional[Union[TextIO, LoggerAsFile]] = sys.stderr,
    skip_cur_frame: bool = False,
    num_context_lines: int = 1,
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
    color_scheme: ColorScheme = ColorSchemes.auto,
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
                color_scheme=choose_color_scheme(color_scheme, file_),
            ):
                file_.write(trace_str)
                file_.write('\n')

            file_.flush()

        if reraise:
            raise e


def prints_tb(
    func__for_noncall_case_only: Optional[Callable] = None,  # to call without "()"
    file_: Optional[Union[TextIO, LoggerAsFile]] = sys.stderr,
    num_context_lines: int = 1,
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
    color_scheme: ColorScheme = ColorSchemes.auto,
):
    if func__for_noncall_case_only:
        return prints_tb(
            file_=file_,
            num_context_lines=num_context_lines,
            max_value_str_len=max_value_str_len,
            max_exc_str_len=max_exc_str_len,
            ellipsis_=ellipsis_,
            color_scheme=choose_color_scheme(color_scheme, file_),
        )(func__for_noncall_case_only)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with printing_tb(
                reraise=True,
                file_=file_,
                skip_cur_frame=True,
                num_context_lines=num_context_lines,
                max_value_str_len=max_value_str_len,
                max_exc_str_len=max_exc_str_len,
                ellipsis_=ellipsis_,
                color_scheme=choose_color_scheme(color_scheme, file_),
            ):
                return func(*args, **kwargs)

        return wrapper

    return decorator
