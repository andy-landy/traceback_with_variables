"""
For the simplest usage possible. Just import it. Handles all environments.
"""

from traceback_with_variables.color import ColorSchemes
from traceback_with_variables.global_hooks import global_print_exc_in_ipython, is_ipython_global
from traceback_with_variables import default_format


try:  # if in ipython or jupyter
    import IPython  # noqa

    default_format.custom_var_printers = [(is_ipython_global, lambda v: None)]
    default_format.color_scheme = ColorSchemes.common
    global_print_exc_in_ipython()

except ModuleNotFoundError:
    default_format.custom_var_printers = [((lambda n, t, fn, is_global: is_global), lambda v: None)]
    global_print_exc()
