import sys
from typing import Optional, Type

from traceback_with_variables.print import print_exc, Format


def global_print_exc(fmt: Optional[Format] = None) -> None:
    sys.excepthook = lambda e_cls, e, tb: print_exc(e=e, fmt=fmt)  # noqa: U100


def global_print_exc_in_ipython(fmt: Optional[Format] = None) -> None:
    try:
        import IPython
    except ModuleNotFoundError:
        raise ValueError("IPython not found")

    IPython.core.interactiveshell.InteractiveShell.showtraceback = \
        lambda self, *args, **kwargs: print_exc(num_skipped_frames=1, fmt=fmt)  # noqa: U100


def in_ipython() -> bool:
    try:
        __IPYTHON__  # noqa
        return True
    except NameError:
        return False


def is_ipython_global(name: str, type_: Type, filename: str, is_global: bool) -> bool:  # noqa: U100
    return is_global and (
        name in ['In', 'Out', 'get_ipython', 'exit', 'quit']
        or name.startswith('_')
    )
