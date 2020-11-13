import inspect
import traceback
from types import TracebackType
from typing import Any, Iterator, Union, Optional

from traceback_with_variables.color import ColorScheme, ColorSchemes


def iter_tb_lines(
    e: Exception,
    tb: Optional[Union[inspect.Traceback, TracebackType]] = None,
    num_skipped_frames: int = 0,
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
    num_context_lines: int = 1,
    color_scheme: ColorScheme = ColorSchemes.none,
    __force_bug_mode: int = 0,  # for tests only
) -> Iterator[str]:
    c = color_scheme

    try:
        yield f'{c.c}Traceback with variables (most recent call last):{c.e}'

        trace = inspect.getinnerframes(tb, context=num_context_lines) \
            if tb else inspect.trace(context=num_context_lines)

        for frame, filename, line_num, func_name, code_lines, func_line_num in trace[num_skipped_frames:]:
            yield f'{c.c}  File "{c.f_}{filename}{c.c_}", line {c.ln_}{line_num}{c.c_}, in {c.fn_}{func_name}{c.e}'

            if code_lines:
                yield f'{c.c}    {c.fs_}{"".join(code_lines).strip()}{c.e}'

            try:
                for var_name, var in frame.f_locals.items():
                    var_str = _to_cropped_str(var, max_value_str_len, max_exc_str_len, ellipsis_)
                    var_lines = var_str.split('\n')
                    yield f'{c.c}      {c.n_}{var_name}{c.c_} = {c.v_}{var_lines[0] if var_lines else var_str}{c.e}'
                    for line in var_lines[1:]:
                        yield f'{c.c}      {c.v_}{line}{c.e}'

                if __force_bug_mode == 1:
                    raise ValueError('force_bug_mode')

            except:  # noqa # indicates a bug in this lib
                yield '    <traceback-with-variables: exception while printing variables>'
                yield f'    {traceback.format_exc()}'

        yield f'{c.ec}{e.__class__.__module__}.{e.__class__.__name__}:{c.et_} {e}{c.e}'

        if __force_bug_mode == 2:
            raise ValueError('force_bug_mode')

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
