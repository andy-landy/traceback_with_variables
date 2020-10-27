import inspect
import logging
import sys
import traceback
from contextlib import contextmanager
from typing import Any, List, Iterator, NoReturn, TextIO, Union


class LoggerAsFile:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def flush(self) -> NoReturn:
        pass

    def write(self, text: str) -> NoReturn:
        for line in text.rstrip('\r\n').split('\n'):
            self.logger.error(line)


@contextmanager
def traceback_with_variables(
    reraise: bool = True,
    file_: Union[TextIO, LoggerAsFile] = sys.stderr,
    flush: bool = False,
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis: str = '...',
):
    try:
        yield

    except Exception as e:
        if file_:
            for trace_str in _iter_trace_strs(
                e=e,
                trace=list(inspect.trace())[1:],
                max_value_str_len=max_value_str_len,
                max_exc_str_len=max_exc_str_len,
                ellipsis=ellipsis,
            ):
                file_.write(trace_str + '\n')

            if flush:
                file_.flush()

        if reraise:
            raise e


def _crop(line: str, max_length: int, ellipsis: str) -> str:
    if len(line) <= max_length or max_length < 0:
        return line

    return line[:max_length] + ellipsis


def _to_cropped_str(obj: Any, max_value_str_len: int, max_exc_str_len: int, ellipsis: str) -> str:
    try:
        return _crop(repr(obj), max_value_str_len, ellipsis)

    except:
        return _crop(
            '<exception while printing> ' + traceback.format_exc(chain=False).replace('\n', '\n  '),
            max_exc_str_len,
            ellipsis,
        )


def _iter_trace_strs(
    e: Exception,
    trace: List,
    max_value_str_len: int,
    max_exc_str_len: int,
    ellipsis: str,
) -> Iterator[str]:
    try:
        yield 'Traceback with variables (most recent call last):'

        for frame, filename, line_num, func_name, code_lines, func_line_num in trace:
            yield f'  File "{filename}", line {line_num}, in {func_name}'

            if code_lines:
                yield '    ' + ''.join(code_lines).rstrip('\r\n').lstrip(' ')  # TODO strip

            try:
                for var_name, var in frame.f_locals.items():
                    var_str = _to_cropped_str(var, max_value_str_len, max_exc_str_len, ellipsis)
                    for line in f'{var_name} = {var_str}'.split('\n'):
                        yield f'      {line}'

            except:  # indicates a bug in this lib
                yield '    <traceback-with-variables: exception while printing variables>'
                yield f'    {traceback.format_exc()}'

        yield f'{e.__class__.__module__}.{e.__class__.__name__}: {e}'

    except:  # indicates a bug in this lib
        yield '    <traceback-with-variables: exception while printing variables>'
        yield f'{traceback.format_exc()}'
