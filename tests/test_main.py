from typing import List

from tests.utils import assert_smart_equals_ref, run_code, run_py


simple_code = '''def f(n):
    m = n - 1
    return 1 / m
a = 3
f(a - 2)'''

status0_code = '''def f(n):
    return n + 1
print(f(10))'''

argparse_code = '''import argparse
def f(n):
    m = n - 1
    return 1 / m
p = argparse.ArgumentParser()
p.add_argument('--a', required=True, type=int)
args = p.parse_args()
a = args.a
f(a - 2)'''


def test_simple_code_no_args(tmp_path):
    _test_code('simple_code_no_args', tmp_path, [], simple_code, [], True)


def test_simple_code_excess_script_args(tmp_path):
    _test_code('simple_code_excess_script_args', tmp_path, [], simple_code, ['--b', '2'], True)


def test_simple_code_tool_args(tmp_path):
    _test_code('simple_code_tool_args', tmp_path, ['--max-value-str-len', '10'], simple_code, [], True)


def test_simple_code_excess_tool_args(tmp_path):
    _test_code('simple_code_excess_tool_args', tmp_path, ['--b', '2'], simple_code, ['pos_arg', '--c', '3'], True)


def test_simple_code_incomplete_tool_args(tmp_path):
    _test_code('simple_code_incomplete_tool_args', tmp_path, ['--max-value-str-len'], simple_code, [], True)


def test_simple_code_tool_help(tmp_path):
    _test_code('simple_code_tool_help', tmp_path, ['--max-value-str-len', '10', '--help'], simple_code, [], False)


def test_argparse_code(tmp_path):
    _test_code('argparse_code', tmp_path, [], argparse_code, ['--a', '3'], True)


def test_argparse_code_script_help(tmp_path):
    _test_code('argparse_code_script_help', tmp_path, [], argparse_code, ['--help'], False)


def test_status0_code(tmp_path):
    _test_code('status0_code', tmp_path, [], status0_code, [], False)


def test_module(tmp_path):
    _test_cmd('module', tmp_path, ['http.server', '--help'], False)


def test_nonexistent(tmp_path):
    _test_cmd('nonexistent', tmp_path, ['nonexistent', '--help'], True)


def test_no_cmd(tmp_path):
    _test_cmd('no_cmd', tmp_path, [], True)


def _test_code(name: str, tmp_path, main_argv: List[str], code: str, code_argv: List[str], raises: bool):
    assert_smart_equals_ref(
        f'test_main.{name}',
        run_code(
            tmp_path=tmp_path,
            python_argv=['-m', 'traceback_with_variables.main'] + main_argv,
            code=code,
            code_argv=code_argv,
            raises=raises
        )
    )


def _test_cmd(name: str, tmp_path, argv: List[str], raises: bool):
    assert_smart_equals_ref(
        f'test_main.{name}',
        run_py(
            tmp_path=tmp_path,
            argv=['-m', 'traceback_with_variables.main'] + argv,
            raises=raises
        )
    )
