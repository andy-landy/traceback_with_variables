import pytest

from traceback_with_variables import core, ColorSchemes, Format

from tests.dummies import Unprintable, f
from tests.utils import assert_smart_equals_ref


def test_default():
    check('default', 10001)


def test_explicit_e():
    try:
        f(10000)
    except Exception as e_:  # noqa
        e = e_

    assert_smart_equals_ref(f'test_core.explicit_e', core.format_exc(e=e))  # noqa


def test_no_e():
    try:
        f(10000)
    except:  # noqa
        pass

    with pytest.raises(ValueError):
        core.format_exc()


# TODO def test_after_unhandled_e():


def test_ellipsis():
    check('ellipsis', 10000, fmt=Format(ellipsis_='*'))


def test_max_value_str_len():
    check('max_value_str_len', 10000, fmt=Format(max_value_str_len=10))


def test_max_exc_str_len():
    check('max_exc_str_len', 10000, fmt=Format(max_exc_str_len=10))


@pytest.mark.parametrize('num_skipped_frames', [0, 1, 2])
def test_num_skipped_frames(num_skipped_frames):
    check(f'num_skipped_frames_{num_skipped_frames}', 10001, num_skipped_frames=num_skipped_frames)


@pytest.mark.parametrize('before', [0, 2, 100])
def test_before(before):
    check(f'before_{before}', 10000, fmt=Format(before=before))


@pytest.mark.parametrize('after', [0, 2, 100])
def test_after(after):
    check(f'after_{after}', 10000, fmt=Format(after=after))


def test_before_after():
    check('before_after', 10000, fmt=Format(before=2, after=2))


def test_color_scheme_common():
    check('color_scheme_common', 10000, fmt=Format(color_scheme=ColorSchemes.common))


def test_color_scheme_synthwave():
    check('color_scheme_synthwave', 10000, fmt=Format(color_scheme=ColorSchemes.synthwave))


def test_color_scheme_nice():
    check('color_scheme_nice', 10000, fmt=Format(color_scheme=ColorSchemes.nice))


@pytest.mark.parametrize('skip_files_except', [None, '.*dummies.*', ['.*test_core.*']])
@pytest.mark.parametrize('brief_files_except', [None, '.*dummies.*', ['.*test_core.*']])
def test_files(skip_files_except, brief_files_except):
    check(f'files_{skip_files_except}_{brief_files_except}', 10000, fmt=Format(
        skip_files_except=skip_files_except,
        brief_files_except=brief_files_except,
    ))


@pytest.mark.parametrize('i1,fs1', enumerate([None, ['s'], ['l', Unprintable], [lambda n, *_: 's' in n]]))
@pytest.mark.parametrize('i2,fs2', enumerate([None, ['s'], ['l', Unprintable], [lambda n, *_: 's' in n]]))
def test_var_printers(i1, fs1, i2, fs2):
    check(f'var_printers_{i1}_{i2}', 10, fmt=Format(
        custom_var_printers=([(fs1, lambda v: None)] if fs1 else []) + ([(fs2, lambda v: 'var')] if fs2 else [])
    ))


@pytest.mark.parametrize('num_skipped_frames', [0, 1])
def test_cur_tb(num_skipped_frames):
    assert_smart_equals_ref(f'test_core.cur_tb_{num_skipped_frames}', get_cur_tb(num_skipped_frames))


def get_cur_tb(num_skipped_frames: int) -> str:
    return core.format_cur_tb(num_skipped_frames=num_skipped_frames, fmt=Format(skip_files_except='test_core'))


def check(name, arg, **kwargs):
    try:
        f(arg)
    except Exception:  # noqa
        assert_smart_equals_ref('test_core.{}'.format(name), core.format_exc(**kwargs))
