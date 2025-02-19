"""
Python Traceback (Error Message) Printing Variables

README.md and examples: https://pypi.org/project/traceback-with-variables
"""

from .color import (  # noqa: F401
    ColorScheme,
    ColorSchemes,
    supports_ansi,
)
from .core import (  # noqa: F401
    Format,
    default_format,
    format_cur_tb,
    format_exc,
    hide,
    iter_cur_tb_lines,
    iter_exc_lines,
    show,
    skip,
)
from .global_hooks import (  # noqa: F401
    global_print_exc,
    global_print_exc_in_ipython,
    is_ipython_global,
)
from .print import (  # noqa: F401
    LoggerAsFile,
    print_cur_tb,
    print_exc,
    printing_exc,
    prints_exc,
)


__version__ = '2.2.0'

# shorter names for swifter interactive usage
fmt = default_format  # noqa
