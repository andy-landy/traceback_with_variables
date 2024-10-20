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


class Reg:
    def __init__(self, label: str) -> None:
        self.label: str = label

    def match_tb_text(self, text: str, sub_label: str = '') -> None:
        self.match_text(strip_tb_text(text), sub_label)
        
    def match_text(self, text: str, sub_label: str = '') -> None:
        path = 'tests/dumps/' + parts_to_fname([self.label, sub_label, 'txt'])
        match_text_in_file(path, text)


def parts_to_fname(parts: List[str]) -> str:
    return ''.join(c if c.isalnum() or c in '.' else '_' for c in '.'.join(p for p in parts if p))


def match_text_in_file(path: str, text: str) -> None:
    if os.getenv('PYTEST_UPDATE_REFS', ''):
        with open(path, 'w') as out:
            out.write(text)

    else:
        with open(path, 'r') as in_:
            old_text = in_.read()
            assert old_text == text


def strip_tb_text(text: str) -> str:
    OFTO = '...omitted for tests only...'
    text = text.replace('\\\\', '\\')  # for windows
    text = re.sub('.:\\\\', '/', text)  # for windows
    text = text.replace('\\', '/')  # for windows
    text = text.replace('\r', '')  # for windows
    text = re.sub(r'\n[^\n]*\^\^\^[^\n]*\n', '\n', text)
    # File "/usr/local/lib/python3.8/dist-packages/_pytest/_code/code.py", line 810, in repr_traceback_entry
    text = re.sub(r'/[\w/.-]+/[\d]+\.py([^\w/-])', fr'{OFTO}\1', text)
    text = re.sub(r'([^\w/.-])/[\w/.-]+(/[\w.-]+[^\w/.-])', fr'\1{OFTO}\2', text)
    text = re.sub(r'/[\w/.-]+(/[\w.-]+\.py[^\w/-])', fr'{OFTO}\1', text)
    text = re.sub(r'(line)[^\n,]+(,)', fr'\1{OFTO}\2', text)
    #text = re.sub(r"(__file__ = )[^\n]*\n", fr"\1'{OFTO}'", text)
    text = re.sub(r'( at 0x)\w+', fr'\1{OFTO}', text)
    #text = re.sub(r'(__builtins__[^{]*{)[^\n]*', fr'\1{OFTO}', text)
    text = re.sub(r'(<ipython-input-)\d+-\w+(>)', fr'{OFTO}', text)
    text = re.sub('\n[^\n]+function open[^\n]+\n', '\n', text)
    text = re.sub('\n[^\n]+_pytest[^\n]+\n', '\n', text)
    #text = re.sub(r'(<_froze?n?s?e?t? ?a?t? ?0?x?).*(>)', fr'\1{OFTO}\2', text)
    #text = re.sub(r'(<trace?b?a?c?k? ?a?t? ?0?x?).*(>)', fr'\1{OFTO}\2', text)
    #text = re.sub(r'(<func?t?i?o?n? ?a?t? ?0?x?).*(>)', fr'\1{OFTO}\2', text)

    return text


@pytest.fixture
def tb_reg(request):
    reg = Reg(label=f'{request.module.__name__}.{request.node.name[5:]}')
    return reg.match_tb_text


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


def run_code_in_ipython(tmp_path, lines: List[str]) -> str:
    out = run_code(tmp_path, ['-m', 'IPython'], lines, [], True)
    out = '\n'.join(out.split('\n')[:-1] + [''])

    return out


def rm_ansi(text: str) -> str:
    return re.sub(r'\033\[.*?m', '', text)


def run_code_in_ipython_2(tmp_path, lines: List[str]) -> str:
    out = run_code_in_ipython(tmp_path, lines)

    return re.sub(r'^.*(f\(\))', r'\1', out, flags=re.S)


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

