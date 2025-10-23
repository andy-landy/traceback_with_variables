import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from subprocess import check_output, CalledProcessError, STDOUT
from typing import Callable, Dict, List, Type

import pytest

import traceback_with_variables

from tests import dummies


dummies_code = Path(dummies.__file__).read_text()
activate_line = 'from traceback_with_variables import activate_by_import'
jupyter_activate_line = 'from traceback_with_variables import activate_in_ipython_by_import'


def type_to_name(type_: Type) -> str:
    return type_.__name__.replace('WindowsPath', 'PosixPath')


def get_min_dur_s(func: Callable, args: List, kwargs: Dict):
    min_dur_s = -1.0

    for _ in range(5):
        start_t_s = time.time()
        func(*args, **kwargs)
        dur_s = time.time() - start_t_s
        min_dur_s = min(min_dur_s, dur_s) if min_dur_s >= 0.0 else dur_s

    return min_dur_s

@dataclass(repr=False)
class Reg:
    dir_path: Path
    label: str
    update: bool

    @classmethod
    def create(cls, label: str):
        update=bool(os.getenv('PYTEST_UPDATE_DUMPS', ''))
        env_name = sys.platform + '_' + '.'.join(sys.version.split('.')[:2])
        dir_path = Path('tests/dumps') / env_name
        if update:
            dir_path.mkdir(parents=True, exist_ok=True)
        return Reg(dir_path=dir_path, label=label, update=update)

    def match_tb_text(self, text: str, sub_label: str = '') -> None:
        self.match_text(strip_tb_text(text), sub_label)
        
    def match_text(self, text: str, sub_label: str = '') -> None:
        label = '.'.join(l for l in [self.label, sub_label] if l)
        path=self.dir_path / (re.sub('[^\w.-]', '-', label) + '.txt')
        if self.update:
            path.write_text(text)
        else:
            assert text == path.read_text()  # open(newline='').read()  # newline='' to keep win32 \r


def strip_tb_text(text: str) -> str:
    OFTO = '...omitted for tests only, '

    text = re.sub(r'\\', '/', text)  # cast win paths so the following rules could apply
    text = re.sub('[A-Z]:/', '/d/', text)  # same
    text = re.sub('\r', '', text)  # cast win lines
    text = re.sub(r'(/argparse.py", line )[^\n,]+(,)', fr'\1{OFTO}argparse internals...\2', text)  # argparse versions
    text = re.sub(r'( at 0x)\w+', fr'\1{OFTO}obj id...', text)  # object ids
    text = re.sub(r'<ipython-input-[^>]+>', f'{OFTO}jupyter cell...', text)  # jupyter cells on some versions
    text = re.sub(r'/[\w/.-]+/\d+.py([^\w/.-])', fr'{OFTO}jupyter cell...\1', text)  # jupyter cells on some versions
    text = re.sub(r'/[\w/.-]+(/[\w.-]+\.py[^\w/.-])', fr'{OFTO}abs path...\1', text)  # machine-dependent paths
    text = re.sub('\n[^\n]+function open[^\n]+\n', '\n', text)  # Jupyter versions?

    return text


@pytest.fixture
def tb_reg(request):
    return Reg.create(label=f'{request.module.__name__}.{request.node.name}').match_tb_text


def set_lib_env(path: Path) -> None:
    for module_path in Path(traceback_with_variables.__file__).parent.parent.glob('*'):
        try:
            (path / module_path.name).symlink_to(module_path)
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
        'notebook', '--output', str(out_path.relative_to(inp_path.parent)), str(inp_path),
    ])
    
    with out_path.open('r') as inp:
        data = json.load(inp)

    return '\n'.join(
        '\n'.join(d['traceback']) if d['output_type'] == 'error' else ''.join(d['text'])
        for d in data['cells'][0]['outputs']
    )

