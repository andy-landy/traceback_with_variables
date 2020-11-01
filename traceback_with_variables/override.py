import os
import sys
from typing import NoReturn

from traceback_with_variables.core import iter_tb_lines


def override_print_tb(
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
    activate_by_env_var: str = '',
    deactivate_by_env_var: str = '',
) -> NoReturn:
    if (activate_by_env_var and not os.getenv(activate_by_env_var, '')) or \
            (deactivate_by_env_var and os.getenv(deactivate_by_env_var, '')):
        return sys.excepthook

    def excepthook(
        e_cls,  # noqa
        e,
        tb
    ):
        for line in iter_tb_lines(
            e=e,
            tb=tb,
            max_value_str_len=max_value_str_len,
            max_exc_str_len=max_exc_str_len,
            ellipsis_=ellipsis_,
        ):
            sys.stderr.write(line)
            sys.stderr.write('\n')

        sys.stderr.flush()

    sys.excepthook = excepthook
