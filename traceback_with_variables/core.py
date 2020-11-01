import inspect
import traceback
from types import TracebackType
from typing import Any, Iterator, Union, Optional


def iter_tb_lines(
    e: Exception,
    tb: Optional[Union[inspect.Traceback, TracebackType]] = None,
    num_skipped_frames: int = 0,
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
    num_context_lines: int = 1,
) -> Iterator[str]:
    try:
        yield 'Traceback with variables (most recent call last):'

        trace = inspect.getinnerframes(tb, context=num_context_lines) \
            if tb else inspect.trace(context=num_context_lines)

        for frame, filename, line_num, func_name, code_lines, func_line_num in trace[num_skipped_frames:]:
            yield f'  File "{filename}", line {line_num}, in {func_name}'

            if code_lines:
                yield '    ' + ''.join(code_lines).rstrip('\r\n').lstrip(' ')  # TODO strip

            try:
                for var_name, var in frame.f_locals.items():
                    var_str = _to_cropped_str(var, max_value_str_len, max_exc_str_len, ellipsis_)
                    for line in f'{var_name} = {var_str}'.split('\n'):
                        yield f'      {line}'

            except:  # noqa # indicates a bug in this lib
                yield '    <traceback-with-variables: exception while printing variables>'
                yield f'    {traceback.format_exc()}'

        yield f'{e.__class__.__module__}.{e.__class__.__name__}: {e}'

    except:  # noqa # indicates a bug in this lib
        yield '    <traceback-with-variables: exception while printing variables>'
        yield f'{traceback.format_exc()}'


def _crop(line: str, max_len: int, ellipsis_: str) -> str:
    if len(line) <= max_len or max_len < 0:
        return line

    return line[:max_len] + ellipsis_


def _to_cropped_str(obj: Any, max_value_str_len: int, max_exc_str_len: int, ellipsis_: str) -> str:
    try:
        return _crop(repr(obj), max_value_str_len, ellipsis_)

    except:  # noqa
        return _crop(
            '<exception while printing> ' + traceback.format_exc(chain=False).replace('\n', '\n  '),
            max_exc_str_len,
            ellipsis_,
        )
