import re
import sys
from typing import List

import pytest

from tests.test_utils import tb_reg, run_code, run_py


RAISING_CODE_LINES = [
    'def f(n):',
    '  m = n + 1',
    '  return 1 / (m - 1)',
    'divide_by_what = 0',
    'f(divide_by_what)',
]

NONRAISING_CODE_LINES = [
    'def f(n):',
    '  m = n + 1',
    '  return 1 / (m - 1)',
    'divide_by_what = 1',
    'f(divide_by_what)',
]

ARGPARSE_CODE_LINES = [
    'import argparse',
    'p = argparse.ArgumentParser()',
    'p.add_argument("--arg", required=True, type=int)',
    'args = p.parse_args()',
    'print("arg", args.arg, "was passed")',
]


def test_raising_code_no_args(do_test_code):
    do_test_code([], RAISING_CODE_LINES, [], True)


def test_raising_code_color_scheme(do_test_code):
    do_test_code(['--color-scheme', 'common'], RAISING_CODE_LINES, [], True)


def test_raising_code_excess_script_args(do_test_code):  # excess args are ignored by this raising code
    do_test_code([], RAISING_CODE_LINES, ['--excess-arg', 'some_value'], True)


def test_raising_code_tool_args(do_test_code):
    # if sys.platform == 'win32':
    #     return
    do_test_code(['--max-value-str-len', '70'], RAISING_CODE_LINES, [], True)


def test_raising_code_tool_args_no_globals(do_test_code):
    do_test_code(['--no-globals'], RAISING_CODE_LINES, [], True)


def test_raising_code_excess_tool_args(do_test_code):
    do_test_code(['--excess-arg', 'some_value'], RAISING_CODE_LINES, ['pos_arg', '--c', '3'], True)


def test_raising_code_incomplete_tool_args(do_test_code):
    do_test_code(['--max-value-str-len'], RAISING_CODE_LINES, [], True)


def test_raising_code_tool_help(do_test_code):
    do_test_code(['--max-value-str-len', '70', '--help'], RAISING_CODE_LINES, [], False)


def test_nonraising_code_no_args(do_test_code):
    do_test_code([], NONRAISING_CODE_LINES, [], False)


def test_nonraising_code_color_scheme(do_test_code):
    do_test_code(['--color-scheme', 'common'], NONRAISING_CODE_LINES, [], False)


def test_nonraising_code_excess_script_args(do_test_code):  # excess args are ignored by this nonraising code
    do_test_code([], NONRAISING_CODE_LINES, ['--excess-arg', 'some_value'], False)


def test_nonraising_code_tool_args(do_test_code):
    # if sys.platform == 'win32':
    #     return
    do_test_code(['--max-value-str-len', '70'], NONRAISING_CODE_LINES, [], False)


def test_nonraising_code_tool_args_no_globals(do_test_code):
    do_test_code(['--no-globals'], NONRAISING_CODE_LINES, [], False)


def test_nonraising_code_excess_tool_args(do_test_code):
    do_test_code(['--excess-arg', 'some_value'], NONRAISING_CODE_LINES, ['pos_arg', '--c', '3'], True)


def test_nonraising_code_incomplete_tool_args(do_test_code):
    do_test_code(['--max-value-str-len'], NONRAISING_CODE_LINES, [], True)


def test_nonraising_code_tool_help(do_test_code):
    do_test_code(['--max-value-str-len', '70', '--help'], RAISING_CODE_LINES, [], False)


def test_argparse_code_ok(do_test_code):
    do_test_code([], ARGPARSE_CODE_LINES, ['--arg', '1'], False)


def test_argparse_code_wrong_args(do_test_code):
    do_test_code([], ARGPARSE_CODE_LINES, ['--wrong', 'value'], True)


def test_argparse_code_script_help(do_test_code):
    do_test_code([], ARGPARSE_CODE_LINES, ['--help'], False)


def test_module(tmp_path, tb_reg):
    out = run_py(
        tmp_path=tmp_path,
        argv=['-m', 'traceback_with_variables.main', 'http.server', '--help'],
        raises=False
    )
    out = re.sub(r'\[([^-][^\s]+) \[[^\s]+ ...]]', r'[\1 ...]', out)
    out = re.sub(r']\s+', ']\n', out).replace('\r', '')
    out = out.replace('[', '(').replace(']', ')').lower().replace(' ', '').replace('alternative', 'alternate')
    #out = re.sub(r'(usage:???why does it change (+/- are reversed)?[^\n]*\(-h\)).*$', fr'\1...', out, flags=re.S)
    out = re.sub('\n\n', '\n', out)
    tb_reg(out)


def test_nonexistent(do_test_cmd):
    do_test_cmd(['nonexistent', '--help'], True)


def test_no_cmd(do_test_cmd):
    do_test_cmd([], True)


@pytest.fixture
def do_test_code(tmp_path, tb_reg):
    def do_test_code_(main_argv: List[str], lines: List[str], code_argv: List[str], raises: bool):
        out = run_code(
            tmp_path=tmp_path,
            python_argv=['-m', 'traceback_with_variables.main'] + main_argv,
            lines=lines,
            code_argv=code_argv,
            raises=raises
        )
        if out.startswith('usage:') and out.count('\n') > 37:  # :)
            lines = out.split('\n')
            out = '\n'.join(lines[:21] + lines[-9:])  # argparse codes differs in py versions
        out = re.sub(r'\[([^-][^\s]+) \[[^\s]+ ...]]', r'[\1 ...]', out)
        out = re.sub(r']\s+', ']\n', out)
        out = out.replace('optional arguments', 'options')
        out = re.sub('(ambiguous option: )[^ ]+( )', fr'\1...', out)
        out = out.replace('required: script, script-arg', 'required: script')
        tb_reg(out)
    
    return do_test_code_


@pytest.fixture
def do_test_cmd(tmp_path, tb_reg):
    def do_test_cmd_(argv: List[str], raises: bool):
        out = run_py(
            tmp_path=tmp_path,
            argv=['-m', 'traceback_with_variables.main'] + argv,
            raises=raises
        )
        out = re.sub(r'\[([^-][^\s]+) \[[^\s]+ ...]]', r'[\1 ...]', out)
        out = re.sub(r']\s+', ']\n', out)
        out = out.replace('required: script, script-arg', 'required: script')
    
    return do_test_cmd_

