"""
For the simplest usage possible. Just import it
"""

from traceback_with_variables.global_hooks import global_print_exc, Format


global_print_exc(fmt=Format(custom_var_printers=[
    ((lambda n, t, fn, is_global: is_global), lambda v: None)
]))
