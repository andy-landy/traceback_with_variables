from typing import List

from tests.utils import assert_smart_equals_ref, run_cmd


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
    run_code(tmp_path, 'simple_code_no_args', simple_code, [], True)


def run_code(tmp_path, name: str, code: str, argv: List[str], raises: bool):
    code_path = tmp_path / 'code.py'
    code_path.write_text(simple_code)

    assert_smart_equals_ref(
        f'test_main.{name}',
        run_cmd(['python3', 'traceback_with_variables/main.py', str(code_path)] + argv, raises=True)
    )

# test module, command, script
