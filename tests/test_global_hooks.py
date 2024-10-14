import re
import sys

import pytest

from tests.test_utils import run_code, run_code_in_jupyter, run_code_in_ipython_2 \
    , dummies_code, activate_line, jupyter_activate_line, tb_reg


_import = 'from traceback_with_variables import '


def test_activate_by_import(tmp_path, tb_reg):
    tb_reg(run_code(tmp_path, [], [_import + 'activate_in_python_by_import', dummies_code, 'f()'], [], True), 'python')
    tb_reg(run_code(tmp_path, [], [_import + 'activate_by_import', dummies_code, 'f()'], [], True), 'common')
    tb_reg(run_code(tmp_path, [], [_import + 'a', dummies_code, 'f()'], [], True), 'short_from')
    tb_reg(run_code(tmp_path, [], ['import traceback_with_variables.a', dummies_code, 'f()'], [], True), 'short_direct')


def test_activate_in_ipython_by_import_error(tmp_path, tb_reg):
    (tmp_path / 'IPython.py').write_text('import nonexistent_module')
    tb_reg(run_code(tmp_path, [], [jupyter_activate_line], [], True))


def test_activate_in_ipython_by_import(tmp_path, tb_reg):
    if sys.platform == 'win32':
        return

    tb_reg(run_code_in_ipython_2(tmp_path, [_import + 'activate_in_ipython_by_import', dummies_code, 'f()']), 'ipython')
    tb_reg(run_code_in_ipython_2(tmp_path, [_import + 'activate_by_import', dummies_code, 'f()']), 'common')
    tb_reg(run_code_in_ipython_2(tmp_path, [_import + 'a', dummies_code, 'f()']), 'short_from')
    tb_reg(run_code_in_ipython_2(tmp_path, ['import traceback_with_variables.a', dummies_code, 'f()']), 'short_direct')


def test_basics_in_jupyter(tmp_path, tb_reg):
    for subname, lines in [
        ('simple', [jupyter_activate_line]),
        ('set fmt attr', [jupyter_activate_line + ', default_format as d', 'd.max_value_str_len = 100']),
        ('shorts', [_import + 'a, fmt', 'fmt.max_value_str_len = 100']),
    ][:1 if sys.platform == 'win32' else 2]:
        tb_reg(run_code_in_jupyter(tmp_path, lines + [dummies_code, 'f()']), subname)

