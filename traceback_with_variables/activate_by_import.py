"""
For the simplest usage possible. Just import it. Handles all environments.
"""

from traceback_with_variables.color import ColorSchemes
from traceback_with_variables.global_hooks import global_print_exc_in_ipython, global_print_exc, is_ipython_global, in_ipython
from traceback_with_variables import default_format


if in_ipython():
    default_format.custom_var_printers = [(is_ipython_global, lambda v: None)]
    default_format.color_scheme = ColorSchemes.common
    global_print_exc_in_ipython()

else:
    default_format.custom_var_printers = [((lambda n, t, fn, is_global: is_global), lambda v: None)]
    global_print_exc()
