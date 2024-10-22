"""
For the simplest usage possible. Jupyter or IPython. Just import it
"""

from traceback_with_variables.color import ColorSchemes
from traceback_with_variables.global_hooks import global_print_exc_in_ipython, is_ipython_global
from traceback_with_variables import default_format


default_format.custom_var_printers = [(is_ipython_global, lambda v: None)]
default_format.color_scheme = ColorSchemes.common
global_print_exc_in_ipython()
