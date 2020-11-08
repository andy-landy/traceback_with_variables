from tests.utils import assert_smart_equals_ref, run_code


def test_activate_by_import(tmp_path):
    code = '''import traceback_with_variables.activate_by_import
def f(n):
    return n / 0
f(10)'''

    assert_smart_equals_ref('test_override.activate_by_import', run_code(tmp_path, [], code, [], True))


def test_deactivate_by_env_var(tmp_path):
    code = '''from traceback_with_variables import override_print_tb
def f(n):
    return n / 0
override_print_tb(activate_by_env_var='NONEXISTENT')
f(10)'''

    assert_smart_equals_ref('test_override.deactivate_by_env_var', run_code(tmp_path, [], code, [], True))
