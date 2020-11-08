import os
import re
from pathlib import Path
from subprocess import check_output, CalledProcessError, STDOUT
from typing import List

import pytest

import traceback_with_variables


def f(a, b):
    print(a)
    print(b)
    assert a == b


def assert_equals_ref(name: str, value: str) -> None:
    path = 'tests/dumps/{}.txt'.format(name)

    if os.getenv('PYTEST_UPDATE_REFS', ''):
        with open(path, 'w') as out:
            out.write(value)

    else:
        with open(path, 'r') as in_:
            f(value, in_.read())


def assert_smart_equals_ref(name: str, value: str) -> None:
    for dir_ in ['traceback_with_variables', 'tests']:
        value = re.sub(r'(File ").*(/{}/)'.format(dir_), r'\1...omitted for tests only...\2', value)
    value = re.sub(r'(File ")((?!\.\.\.).)*"'.format(dir_), r'\1...omitted for tests only..."', value)
    value = re.sub(r"'/.*\.py'", "'/...omitted for tests only...py'", value)
    value = re.sub(r'( at 0x)\w+', r'\1...omitted for tests only...', value)

    assert_equals_ref(name, value)


def run_code(tmp_path, python_argv: List[str], code: str, code_argv: List[str], raises: bool = False) -> str:
    (tmp_path / 'traceback_with_variables').symlink_to(Path(traceback_with_variables.__file__).parent)
    code_path = tmp_path / 'code.py'
    code_path.write_text(code)

    return run_cmd(argv=['python3'] + python_argv + [code_path] + code_argv, raises=raises)


def run_cmd(argv: List[str], raises: bool = False):
    if raises:
        with pytest.raises(CalledProcessError) as e:
            check_output(argv, stderr=STDOUT)

        return e.value.output.decode('utf-8')

    return check_output(argv, stderr=STDOUT).decode('utf-8')
