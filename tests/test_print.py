import logging
import sys
from io import StringIO

import pytest

from traceback_with_variables.print import printing_exc, prints_exc, print_cur_tb, LoggerAsFile, Format

from tests.utils import assert_smart_equals_ref, run_code


def test_print_cur_tb():
    out = StringIO()
    get_cur_tb(out)

    assert_smart_equals_ref('test_print.print_cur_tb', out.getvalue())


def get_cur_tb(out):
    x = 10
    return print_cur_tb(fmt=Format(skip_files_except='test_print'), file_=out)


def test_printing_exc():
    out = StringIO()
    with printing_exc(reraise=False, file_=out):
        f(10)

    assert_smart_equals_ref('test_print.printing_exc', out.getvalue())


def test_printing_exc_to_tty():
    if sys.platform == 'win32':
        return

    out = StringIO()
    out.isatty = lambda: True
    with printing_exc(reraise=False, file_=out):
        f(10)

    assert_smart_equals_ref('test_print.printing_exc_to_tty', out.getvalue())


def test_printing_exc_stderr(tmp_path):
    code = '''from traceback_with_variables import printing_exc
def f(n):
    return n / 0
    
def main():
    with printing_exc(reraise=False):
        return f(10)
         
main()'''

    assert_smart_equals_ref('test_print.printing_exc_stderr', run_code(tmp_path, [], code, [], False))


def test_printing_exc_reraise():
    out = StringIO()
    with pytest.raises(ZeroDivisionError):
        with printing_exc(reraise=True, file_=out):
            f(10)


def test_printing_exc_skip_cur_frame():
    out = StringIO()
    with printing_exc(reraise=False, file_=out, skip_cur_frame=True):
        f(10)

    assert_smart_equals_ref('test_print.printing_exc_skip_cur_frame', out.getvalue())


def test_prints_exc():
    out = StringIO()
    with pytest.raises(ZeroDivisionError):
        prints_exc(file_=out)(f)(10)

    assert_smart_equals_ref('test_print.prints_exc', out.getvalue())


def test_prints_exc_noncall(tmp_path):
    code = '''from traceback_with_variables import prints_exc
@prints_exc
def f(n):
    return n / 0
try:
    f(10)
except:
    pass'''

    assert_smart_equals_ref('test_print.prints_exc_noncall', run_code(tmp_path, [], code, [], False))


def test_logger_as_file(caplog):
    with printing_exc(reraise=False, file_=LoggerAsFile(logging.getLogger('test-logger'))):
        f(10)

    assert_smart_equals_ref('test_print.logger_as_file', caplog.text)


def test_logger_as_file_lines(caplog):
    with printing_exc(reraise=False, file_=LoggerAsFile(logging.getLogger('test-logger'), separate_lines=True)):
        f(10)

    assert_smart_equals_ref('test_print.logger_as_file_lines', caplog.text)


def f(n):
    return n / 0
