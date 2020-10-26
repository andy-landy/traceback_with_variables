import logging
import os
import re
from io import StringIO

import pytest

from rich_traceback import rich_traceback, LoggerAsFile


def test_file():
    out = StringIO()
    with rich_traceback(reraise=False, file_=out):
        f(10001)

    assert_smart_equals_ref('test_file', out.getvalue())


def test_ellipsis():
    out = StringIO()
    with rich_traceback(reraise=False, file_=out, ellipsis='*'):
        f(10000)

    assert_smart_equals_ref('test_ellipsis', out.getvalue())


def test_max_value_str_len():
    out = StringIO()
    with rich_traceback(reraise=False, file_=out, max_value_str_len=10):
        f(10000)

    assert_smart_equals_ref('test_max_value_str_len', out.getvalue())


def test_max_exc_str_len():
    out = StringIO()
    with rich_traceback(reraise=False, file_=out, max_exc_str_len=10):
        f(10000)

    assert_smart_equals_ref('test_max_exc_str_len', out.getvalue())


def test_reraise():
    out = StringIO()

    with pytest.raises(ZeroDivisionError):
        with rich_traceback(reraise=True, file_=out):
            f(10000)

    assert_smart_equals_ref('test_reraise', out.getvalue())


def test_logger(caplog):
    with rich_traceback(reraise=False, file_=LoggerAsFile(logging.getLogger('test-logger'))):
        f(10000)

    assert_smart_equals_ref('test_logger', caplog.text)

# - playground - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def f(n: int) -> int:
    s1 = 'short string with n={}'.format(n)
    l1 = 'long string with 0..n: {}'.format(', '.join(map(str, range(n))))
    us = [Unprintable(), Unprintable(), Unprintable()]

    if n % 10 == 0:
        return 1 // (n * 0)

    if n % 2 == 0:
        return f(n - 1)
    else:
        return f(
            n

            - 1
        )


class Unprintable:
    def __repr__(self):
        raise ValueError("please don't print me")


# - utils - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def assert_equals_ref(name: str, value: str) -> None:
    path = 'tests/{}.dump.txt'.format(name)

    if os.getenv('PYTEST_UPDATE_REFS', ''):
        with open(path, 'w') as out:
            out.write(value)

    else:
        with open(path, 'r') as in_:
            assert value == in_.read()


def hide_paths(text: str) -> str:
    return text.replace(os.path.abspath(os.path.curdir), '.')


def hide_objs(text: str) -> str:
    return re.sub(r'object at 0x\w+', 'object at 0x???', text)


def assert_smart_equals_ref(name: str, value: str) -> None:
    assert_equals_ref(name, hide_objs(hide_paths(value)))
