import os
from subprocess import check_output, CalledProcessError, STDOUT

import pytest

from tests.utils import assert_smart_equals_ref


def test_activate_by_import(tmp_path):
    code_path = tmp_path / 'code.py'
    code_path.write_text('''import traceback_with_variables.activate_by_import
def f(n):
    return n / 0
f(10)''')

    with pytest.raises(CalledProcessError) as e:
        check_output(['python3', code_path], stderr=STDOUT, env={'PYTHONPATH': os.getcwd()})

    assert_smart_equals_ref('test_override.activate_by_import', e.value.output.decode('utf-8'))
