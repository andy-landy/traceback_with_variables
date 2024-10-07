import re
import sys

from tests.utils import assert_smart_equals_ref, run_code, run_code_in_jupyter, rm_ansi \
    , dummies_code, activate_line, jupyter_activate_line


def test_activate_by_import(tmp_path):
    code = [activate_line, dummies_code, 'f(10000)']
    assert_smart_equals_ref('test_global_hooks.activate_by_import', run_code(tmp_path, [], code, [], True))


def test_activate_in_ipython_by_import_error(tmp_path):
    (tmp_path / 'IPython.py').write_text('import nonexistent_module')
    assert_smart_equals_ref('test_global_hooks.activate_in_ipython_by_import_error'
                            '', run_code(tmp_path, [], [jupyter_activate_line], [], True))


def test_activate_ipython_by_import_win32(tmp_path):
    _test_activate_in_ipython_by_import(tmp_path, 'test_global_hooks.activate_in_ipython_by_import_win32', True)


def test_activate_ipython_by_import_no_win32(tmp_path):
    _test_activate_in_ipython_by_import(tmp_path, 'test_global_hooks.activate_in_ipython_by_import_no_win32', False)


def _test_activate_in_ipython_by_import(tmp_path, name, win32: bool):
    if (not win32) and sys.platform == 'win32':
        return

    code = [jupyter_activate_line, dummies_code, 'f(10000)']
    out = run_code(tmp_path, ['-m', 'IPython'], code, [], True)
    out = '\n'.join(out.split('\n')[:-1] + [''])
    if win32:
        out = rm_ansi(out)

    assert_smart_equals_ref(name, re.sub(r'^.*(variables\.activate)', r'\1', out, flags=re.S))


def test_basics_in_jupyter(tmp_path):
    def run(subname, lines):
        assert_smart_equals_ref(
            'test_global_hooks.test_basics_in_jupyter.' + subname,
            run_code_in_jupyter(tmp_path, lines + [dummies_code, 'f(10001)']),
        )

    run('simple', [jupyter_activate_line])
    run('set fmt attr', [jupyter_activate_line + ', default_format', 'default_format.max_value_str_len = 10'])


