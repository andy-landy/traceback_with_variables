import os
import sys
from typing import NoReturn

from traceback_with_variables.color import choose_color_scheme
from traceback_with_variables.core import iter_tb_lines, ColorScheme, ColorSchemes


def override_print_tb(
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
    num_context_lines: int = 1,
    activate_by_env_var: str = '',
    deactivate_by_env_var: str = '',
    color_scheme: ColorScheme = ColorSchemes.auto,
    ipython: bool = False,  # for Jupyter or IPython
) -> NoReturn:
    if (activate_by_env_var and not os.getenv(activate_by_env_var, '')) or \
            (deactivate_by_env_var and os.getenv(deactivate_by_env_var, '')):
        return

    def print_tb(e, tb, num_skipped_frames: int) -> NoReturn:
        for line in iter_tb_lines(
            e=e,
            tb=tb,
            num_context_lines=num_context_lines,
            max_value_str_len=max_value_str_len,
            max_exc_str_len=max_exc_str_len,
            ellipsis_=ellipsis_,
            color_scheme=choose_color_scheme(color_scheme, sys.stderr),
            num_skipped_frames=num_skipped_frames,
        ):
            sys.stderr.write(line)
            sys.stderr.write('\n')

        sys.stderr.flush()

    if ipython:
        try:
            import IPython
        except ModuleNotFoundError:
            raise ValueError("ipython=True, but IPython not found")

        IPython.core.interactiveshell.InteractiveShell.showtraceback = \
            lambda self, *args, **kwargs: print_tb(None, None, 1)  # noqa

    else:
        sys.excepthook = lambda e_cls, e, tb: print_tb(e, tb, 0)  # noqa
