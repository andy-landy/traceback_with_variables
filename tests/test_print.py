import logging
import sys
from io import StringIO

import pytest

from traceback_with_variables.print import printing_exc, prints_exc, print_cur_tb, LoggerAsFile, Format

from tests.dummies import f
from tests.test_utils import tb_reg, run_code


def test_print_cur_tb(tb_reg):
    out = StringIO()
    get_cur_tb(out)
    tb_reg(out.getvalue())


def get_cur_tb(out):
    x = 10
    return print_cur_tb(fmt=Format(skip_files_except='test_print'), file_=out)


def test_printing_exc(tb_reg):
    out = StringIO()
    with printing_exc(reraise=False, file_=out):
        f()
    tb_reg(out.getvalue())


def test_printing_exc_to_tty(tb_reg):
    if sys.platform == 'win32':
        return

    out = StringIO()
    out.isatty = lambda: True
    with printing_exc(reraise=False, file_=out):
        f()

    tb_reg(out.getvalue())


def test_printing_exc_stderr(tb_reg, tmp_path):
    lines = [
        'from traceback_with_variables import printing_exc',
        'def f(n):',
        '  return n / 0',
        'def main():',
        '  with printing_exc(reraise=False):',
        '    return f(10)',
        'main()',
    ]

    tb_reg(run_code(tmp_path, [], lines, [], False))


def test_printing_exc_reraise():
    out = StringIO()
    with pytest.raises(ZeroDivisionError):
        with printing_exc(reraise=True, file_=out):
            f()


def test_printing_exc_skip_cur_frame(tb_reg):
    out = StringIO()
    with printing_exc(reraise=False, file_=out, skip_cur_frame=True):
        f()

    tb_reg(out.getvalue())


def test_prints_exc(tb_reg):
    out = StringIO()
    with pytest.raises(ZeroDivisionError):
        prints_exc(file_=out)(f)()

    tb_reg(out.getvalue())


def test_prints_exc_noncall(tmp_path, tb_reg):
    lines = [
        'from traceback_with_variables import prints_exc',
        '@prints_exc',
        'def f(n):',
        '  return n / 0',
        'try:',
        '  f(10)',
        'except:',
        '  pass',
    ]

    tb_reg(run_code(tmp_path, [], lines, [], False))


def test_logger_as_file(caplog, tb_reg):
    with printing_exc(reraise=False, file_=LoggerAsFile(logging.getLogger('test-logger'))):
        f()

    tb_reg(caplog.text)


def test_logger_as_file_lines(caplog, tb_reg):
    with printing_exc(reraise=False, file_=LoggerAsFile(logging.getLogger('test-logger'), separate_lines=True)):
        f()

    tb_reg(caplog.text)

