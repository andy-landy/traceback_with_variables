import os
import re


def assert_equals_ref(name: str, value: str) -> None:
    path = 'tests/dumps/{}.txt'.format(name)

    if os.getenv('PYTEST_UPDATE_REFS', ''):
        with open(path, 'w') as out:
            out.write(value)

    else:
        with open(path, 'r') as in_:
            assert value == in_.read()


def assert_smart_equals_ref(name: str, value: str) -> None:
    for dir_ in ['traceback_with_variables', 'tests']:
        value = re.sub(r'(File ").*(/{}/)'.format(dir_), r'\1...\2', value)
    value = re.sub(r'(object at 0x)\w+', r'\1...', value)

    assert_equals_ref(name, value)
