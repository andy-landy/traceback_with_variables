from tests.utils import assert_smart_equals_ref, run_code


def test_activate_by_import(tmp_path):
    code = '''import traceback_with_variables.activate_by_import
def f(n):
    return n / 0
f(10)'''

    assert_smart_equals_ref('test_override.activate_by_import', run_code(tmp_path=tmp_path, code=code, raises=True))
