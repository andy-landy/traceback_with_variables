from traceback_with_variables.core import iter_tb_lines

from tests.utils import assert_smart_equals_ref


def test_default():
    check('default', 10001)


def test_ellipsis():
    check('ellipsis', 10000, ellipsis_='*')


def test_max_value_str_len():
    check('max_value_str_len', 10000, max_value_str_len=10)


def test_max_exc_str_len():
    check('max_exc_str_len', 10000, max_exc_str_len=10)


def test_num_skipped_frames():
    check('num_skipped_frames', 10001, num_skipped_frames=1)


def test_num_context_lines():
    check('num_context_lines', 10000, num_context_lines=5)


def check(name, arg, **kwargs):
    try:
        f(arg)
    except Exception as e:  # noqa
        assert_smart_equals_ref('test_core.{}'.format(name), '\n'.join(iter_tb_lines(e, **kwargs)))


def f(n: int) -> int:
    s1 = 'short string with n: {}'.format(n)
    l1 = 'long string with 0..n: {}'.format(', '.join(map(str, range(n))))
    us = [Unprintable(), Unprintable(), Unprintable()]

    if n % 10 == 0:
        return 1 // (n * 0)

    if n % 2 == 0:
        return f(n - 1)
    else:
        return f(
            n

            - 1
        )


class Unprintable:
    def __repr__(self):
        raise ValueError("please don't print me")
