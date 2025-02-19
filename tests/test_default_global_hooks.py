import pytest

from traceback_with_variables import fmt, format_exc

from tests.test_utils import tb_reg


def f(n = 1):
    money = '1000'
    password = 'qwerty'
    secret_word = 'please'
    monkey_species = 'gorilla'
    my_pAssWOrd_2 = 'qwerty'
    mySecretN = 5
    card_number = '1234 5678 1234 5678'

    if n > 0:
        return f(n - 1)

    raise ValueError('planned exception')


def check(tb_reg, fmt):
    try:
        f()
    except Exception:  # noqa
        tb_reg(format_exc(fmt=fmt))


def test_patterns_to_hide(tb_reg):
    check(tb_reg, fmt)
