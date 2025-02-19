from traceback_with_variables.color import ColorSchemes
from traceback_with_variables.core import skip
from traceback_with_variables.global_hooks import (
    global_print_exc_in_ipython,
    global_print_exc,
    is_ipython_global,
    in_ipython,
)
from traceback_with_variables import default_format


def default_global_print_exc():
    default_format.custom_var_printers += [
        ((lambda n, t, fn, is_global: is_global), skip),  # noqa: U100
    ]
    global_print_exc()


def default_global_print_exc_in_ipython():
    default_format.custom_var_printers += [
        (is_ipython_global, skip),
    ]
    default_format.color_scheme = ColorSchemes.common
    global_print_exc_in_ipython()


def default_global_print_exc_in_all():
    (default_global_print_exc_in_ipython if in_ipython() else default_global_print_exc)()
