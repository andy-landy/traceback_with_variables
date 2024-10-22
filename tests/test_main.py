import re
import sys
from typing import List

import pytest

from tests.test_utils import tb_reg, run_code, run_py


simple_lines = [
    'def f(n):',
    '  m = n - 1',
    '  return 1 / m',
    'a = 3',
    'f(a - 2)',
]

status0_lines = [
    'def f(n):',
    '  return n + 1',
    'print(f(10))',
]

argparse_lines = [
    'import argparse',
    'def f(n):',
    '  m = n - 1',
    '  return 1 / m',
    'p = argparse.ArgumentParser()',
    'p.add_argument("--a", required=True, type=int)',
    'args = p.parse_args()',
    'a = args.a',
    'f(a - 2)',
]


def test_simple_code_no_args(do_test_code):
    do_test_code([], simple_lines, [], True)


def test_simple_code_color_scheme(do_test_code):
    do_test_code(['--color-scheme', 'common'], simple_lines, [], True)


def test_simple_code_excess_script_args(do_test_code):
    do_test_code([], simple_lines, ['--b', '2'], True)


def test_simple_code_tool_args(do_test_code):
    if sys.platform == 'win32':
        return
    do_test_code(['--max-value-str-len', '70'], simple_lines, [], True)


def test_simple_code_tool_args_no_globals(do_test_code):
    do_test_code(['--no-globals'], simple_lines, [], True)


def test_simple_code_excess_tool_args(do_test_code):
    do_test_code(['--b', '2'], simple_lines, ['pos_arg', '--c', '3'], True)


def test_simple_code_incomplete_tool_args(do_test_code):
    do_test_code(['--max-value-str-len'], simple_lines, [], True)


def test_simple_code_tool_help(do_test_code):
    do_test_code(['--max-value-str-len', '70', '--help'], simple_lines, [], False)


def test_argparse_code(do_test_code):
    do_test_code([], argparse_lines, ['--a', '3'], True)


def test_argparse_code_script_help(do_test_code):
    do_test_code([], argparse_lines, ['--help'], False)


def test_status0_code(do_test_code):
    do_test_code([], status0_lines, [], False)


def test_module(tmp_path, tb_reg):
    out = run_py(
        tmp_path=tmp_path,
        argv=['-m', 'traceback_with_variables.main', 'http.server', '--help'],
        raises=False
    )
    out = re.sub(r'\[([^-][^\s]+) \[[^\s]+ ...]]', r'[\1 ...]', out)
    out = re.sub(r']\s+', ']\n', out).replace('\r', '')
    out = out.replace('[', '(').replace(']', ')').lower().replace(' ', '').replace('alternative', 'alternate')
    out = re.sub(r'(usage:server.py\(-h\)).*$', fr'\1...', out, flags=re.S)
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

