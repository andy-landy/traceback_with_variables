import json
import os
import re
import sys
from pathlib import Path
from subprocess import check_output, CalledProcessError, STDOUT
from typing import List

import pytest

import traceback_with_variables

from tests import dummies


dummies_code = Path(dummies.__file__).read_text()
activate_line = 'from traceback_with_variables import activate_by_import'
jupyter_activate_line = 'from traceback_with_variables import activate_in_ipython_by_import'


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
    value = re.sub(r"(__file__ = )[^\n]*\n", r"\1'...omitted for tests only...'", value)
    value = re.sub(r'( at 0x)\w+', r'\1...omitted for tests only...', value)
    value = re.sub(r'(__builtins__[^{]*{)[^\n]*', r'\1...omitted for tests only...}', value)
    value = re.sub(r'(<ipython-input-)\d+-\w+(>)', r'\1...omitted for test only...\2', value)

    assert_equals_ref(name, value)


def set_lib_env(path: Path) -> None:
    try:
        (path / 'traceback_with_variables').symlink_to(Path(traceback_with_variables.__file__).parent)
    except FileExistsError:
        pass


def run_code(tmp_path, python_argv: List[str], lines: List[str], code_argv: List[str], raises: bool = False) -> str:
    code_path = tmp_path / 'code.py'
    code_path.write_text('\n'.join(lines))

    return run_py(tmp_path=tmp_path, argv=python_argv + [str(code_path)] + code_argv, raises=raises)


def run_py(tmp_path, argv: List[str], raises: bool = False) -> str:
    set_lib_env(tmp_path)

    return run_cmd(argv=['python' + ('' if 'win' in sys.platform else '3')] + argv, raises=raises)


def run_cmd(argv: List[str], raises: bool = False) -> str:
    if raises:
        with pytest.raises(CalledProcessError) as e:
            check_output(argv, stderr=STDOUT)

        return e.value.output.decode('utf-8')

    return check_output(argv, stderr=STDOUT).decode('utf-8')


def rm_ansi(text: str) -> str:
    return re.sub(r'\033\[.*?m', '', text)


def py_code_to_ipynb_code(lines: List[str]) -> str:
    source_lines = [l + ('' if (i == len(lines) - 1) else '\n') for i, l in enumerate(lines)]

    return json.dumps({
        "cells":[{"cell_type":"code","execution_count":None,"id":"focused-print","metadata":{},
        "outputs":[],"source":source_lines}],"metadata":{"kernelspec":{"display_name":"Python 3",
        "language":"python","name":"python3"},"language_info":{"codemirror_mode":{"name":"ipython",
        "version":3},"file_extension":".py","mimetype":"text/x-python","name":"python",
        "nbconvert_exporter":"python","pygments_lexer":"ipython3","version":"3.8.10"}},
        "nbformat":4,"nbformat_minor":5
    })


def run_code_in_jupyter(tmp_path, lines: List[str]) -> str:
    set_lib_env(tmp_path)
    
    inp_path = tmp_path / 'input.ipynb'
    inp_path.write_text(py_code_to_ipynb_code(lines))

    out_path = tmp_path / 'output.ipynb'
    run_cmd([
        'jupyter', 'nbconvert', '--execute', '--allow-errors', '--to',
        'notebook', '--output', out_path.relative_to(inp_path.parent), str(inp_path),
    ])
    
    with out_path.open('r') as inp:
        data = json.load(inp)

    return '\n'.join(
        '\n'.join(d['traceback']) if d['output_type'] == 'error' else ''.join(d['text'])
        for d in data['cells'][0]['outputs']
    )

