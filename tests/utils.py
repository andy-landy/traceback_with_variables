import os
import re
import sys
from pathlib import Path
from subprocess import check_output, CalledProcessError, STDOUT
from typing import List

import pytest

import traceback_with_variables


def assert_eq(v1, v2):  # o_O
    if v1 != v2:
        print('left =', v1)
        print('right =', v2)

    assert v1 == v2


def assert_equals_ref(name: str, value: str) -> None:
    path = 'tests/dumps/{}.txt'.format(''.join(c if c.isalnum() or c in '.' else '_' for c in name))

    if os.getenv('PYTEST_UPDATE_REFS', ''):
        with open(path, 'w') as out:
            out.write(value)

    else:
        with open(path, 'r') as in_:
            assert_eq(value, in_.read())


def assert_smart_equals_ref(name: str, value: str) -> None:
    value = value.replace('\\\\', '\\')  # for windows
    value = re.sub('.:\\\\', '/', value)  # for windows
    value = value.replace('\\', '/')  # for windows
    value = value.replace('\r', '')  # for windows
    for dir_ in ['traceback_with_variables', 'tests']:
        value = re.sub(r'(File ").*(/{}/)'.format(dir_), r'\1...omitted for tests only...\2', value)
    value = re.sub(r'(File ")((?!\.\.\.).)*"'.format(dir_), r'\1...omitted for tests only..."', value)
    value = re.sub(r"'/.*\.py'", "'/...omitted for tests only...py'", value)
    value = re.sub(r'( at 0x)\w+', r'\1...omitted for tests only...', value)
    value = re.sub(r'(__builtins__[^{]*{)[^\n]*', r'\1...omitted for tests only...}', value)

    assert_equals_ref(name, value)


def run_code(tmp_path, python_argv: List[str], code: str, code_argv: List[str], raises: bool = False) -> str:
    code_path = tmp_path / 'code.py'
    code_path.write_text(code)

    return run_py(tmp_path=tmp_path, argv=python_argv + [str(code_path)] + code_argv, raises=raises)


def run_py(tmp_path, argv: List[str], raises: bool = False) -> str:
    (tmp_path / 'traceback_with_variables').symlink_to(Path(traceback_with_variables.__file__).parent)

    return run_cmd(argv=['python' + ('' if 'win' in sys.platform else '3')] + argv, raises=raises)


def run_cmd(argv: List[str], raises: bool = False) -> str:
    if raises:
        with pytest.raises(CalledProcessError) as e:
            check_output(argv, stderr=STDOUT)

        return e.value.output.decode('utf-8')

    return check_output(argv, stderr=STDOUT).decode('utf-8')


def rm_ansi(text: str) -> str:
    return re.sub(r'\033\[.*?m', '', text)
