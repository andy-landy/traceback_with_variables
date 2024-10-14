"""
For the simplest usage possible. Just import it. For 'python3' command usage, not for Jupyter or IPython
"""

from traceback_with_variables.global_hooks import global_print_exc
from traceback_with_variables import default_format


default_format.custom_var_printers = [((lambda n, t, fn, is_global: is_global), lambda v: None)]
global_print_exc()
