import re
import sys

from tests.utils import assert_smart_equals_ref, run_code, rm_ansi


def test_activate_by_import(tmp_path):
    code = '''import traceback_with_variables.activate_by_import
def f(n):
    return n / 0
f(10)'''

    assert_smart_equals_ref('test_global_hooks.activate_by_import', run_code(tmp_path, [], code, [], True))


def test_activate_in_ipython_by_import_error(tmp_path):
    code = '''import traceback_with_variables.activate_in_ipython_by_import'''

    (tmp_path / 'IPython.py').write_text('import nonexistent_module')
    assert_smart_equals_ref('test_global_hooks.activate_in_ipython_by_import_error'
                            '', run_code(tmp_path, [], code, [], True))


def test_activate_ipython_by_import_win32(tmp_path):
    _test_activate_in_ipython_by_import(tmp_path, 'test_global_hooks.activate_in_ipython_by_import_win32', True)


def test_activate_ipython_by_import_no_win32(tmp_path):
    _test_activate_in_ipython_by_import(tmp_path, 'test_global_hooks.activate_in_ipython_by_import_no_win32', False)


def _test_activate_in_ipython_by_import(tmp_path, name, win32: bool):
    if (not win32) and sys.platform == 'win32':
        return

    code = '''from traceback_with_variables import activate_in_ipython_by_import
def f(n):
    return n / 0
f(10)'''

    out = run_code(tmp_path, ['-m', 'IPython'], code, [], True)
    out = '\n'.join(out.split('\n')[:-1] + [''])
    if win32:
        out = rm_ansi(out)

    assert_smart_equals_ref(name, re.sub(r'^.*(variables\.activate)', r'\1', out, flags=re.S))
