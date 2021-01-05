"""
For the simplest usage possible. Just import it
"""

from traceback_with_variables.color import ColorSchemes
from traceback_with_variables.global_hooks import global_print_exc_in_ipython, Format, is_ipython_global

global_print_exc_in_ipython(fmt=Format(
    custom_var_printers=[(is_ipython_global, lambda v: None)],
    color_scheme=ColorSchemes.common
))
