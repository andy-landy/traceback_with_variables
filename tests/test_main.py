from typing import List

from tests.utils import assert_smart_equals_ref, run_code


simple_code = '''def f(n):
    m = n - 1
    return 1 / m
a = 3
f(a - 2)'''

simple_status0_code = '''def f(n):
    return n + 1
print(f(10))'''

code_with_argparse = '''import argparse
def f(n):
    m = n - 1
    return 1 / m
p = argparse.ArgumentParser()
p.add_argument('--a', required=True)
args = p.parse_args()
a = args.a
f(a - 2)'''


def test_simple_code_no_args(tmp_path):
    _test('simple_code_no_args', tmp_path, [], simple_code, [], True)


def _test(name: str, tmp_path, main_argv: List[str], code: str, code_argv: List[str], raises: bool):
    assert_smart_equals_ref(
        f'test_main.{name}',
        run_code(
            tmp_path=tmp_path,
            python_argv=['traceback_with_variables/main.py'] + main_argv,
            code=code,
            code_argv=code_argv,
            raises=raises
        )
    )

# test module, command, script
