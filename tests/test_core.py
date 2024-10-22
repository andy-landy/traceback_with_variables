import pytest

from traceback_with_variables import core, ColorSchemes, Format

from tests.dummies import Unprintable, f, A
from tests.test_utils import tb_reg


@pytest.fixture
def check(tb_reg):
    def check_(**kwargs):
        try:
            f()
        except Exception:  # noqa
            tb_reg(core.format_exc(**kwargs))

    return check_


def test_replace():
    fmt = Format(
        max_value_str_len=1,
        objects_details=1,
        ellipsis_rel_pos=0.5,
        max_exc_str_len=1,
        ellipsis_='.',
        before=1,
        after=1,
        color_scheme=None,
        skip_files_except=[],
        brief_files_except=[],
        custom_var_printers=[],
    )
    fmt2 = fmt.replace(
        before=2,
        skip_files_except=['f1', 'f2'],
    )
    assert fmt.max_value_str_len == fmt.max_value_str_len
    assert fmt2.before == 2
    assert fmt.before == 1
    assert fmt2.skip_files_except == ['f1', 'f2']
    assert fmt.skip_files_except == []


def test_setattr():
    fmt = Format()
    fmt.max_value_str_len = 1
    fmt.objects_details = 1
    fmt.ellipsis_rel_pos = 0.5
    fmt.max_exc_str_len = 1
    fmt.ellipsis_ = '.'
    fmt.before = 1
    fmt.after = 1
    fmt.color_scheme = None
    fmt.skip_files_except = []
    fmt.brief_files_except = []
    fmt.custom_var_printers = []
    with pytest.raises(AttributeError):
        fmt.max_val_str_len = 1


def test_default(check):
    check()


def test_explicit_e(tb_reg):
    try:
        f()
    except Exception as e_:  # noqa
        e = e_

    tb_reg(core.format_exc(e=e))  # noqa


def test_no_e():
    try:
        f()
    except:  # noqa
        pass

    with pytest.raises(ValueError):
        core.format_exc()


# TODO def test_after_unhandled_e():


def test_ellipsis(check):
    check(fmt=Format(ellipsis_='*'))


def test_max_value_str_len(check):
    check(fmt=Format(max_value_str_len=100))


@pytest.mark.parametrize('obj', [[1, 2, 3], A(11, 12), A(A(11, 12), A(13, 14)), A(Unprintable(), 2)])
@pytest.mark.parametrize('objects_details', [0, 1, 10])
def test_objects_details(tb_reg, obj, objects_details):
    try:
        1/0
    except:
        tb_reg(core.format_exc(fmt=Format(objects_details=objects_details)))


@pytest.mark.parametrize('ellipsis_rel_pos', [-0.5, 0.0, 0.5, 0.7, 1.0, 1.5])
def test_ellipsis_rel_pos(check, ellipsis_rel_pos):
    check(fmt=Format(ellipsis_rel_pos=ellipsis_rel_pos))


def test_max_exc_str_len(check):
    check(fmt=Format(max_exc_str_len=50))


@pytest.mark.parametrize('num_skipped_frames', [0, 1, 2])
def test_num_skipped_frames(check, num_skipped_frames):
    check(num_skipped_frames=num_skipped_frames)


@pytest.mark.parametrize('before', [0, 2, 100])
def test_before(check, before):
    check(fmt=Format(before=before))


@pytest.mark.parametrize('after', [0, 2, 100])
def test_after(check, after):
    check(fmt=Format(after=after))


def test_before_after(check):
    check(fmt=Format(before=2, after=2))


def test_color_scheme_common(check):
    check(fmt=Format(color_scheme=ColorSchemes.common))


def test_color_scheme_synthwave(check):
    check(fmt=Format(color_scheme=ColorSchemes.synthwave))


def test_color_scheme_nice(check):
    check(fmt=Format(color_scheme=ColorSchemes.nice))


@pytest.mark.parametrize('skip_files_except', [None, '.*dummies.*', ['.*test_core.*']])
@pytest.mark.parametrize('brief_files_except', [None, '.*dummies.*', ['.*test_core.*']])
def test_files(check, skip_files_except, brief_files_except):
    check(fmt=Format(skip_files_except=skip_files_except, brief_files_except=brief_files_except))


@pytest.mark.parametrize('i1,fs1', enumerate([None, ['s'], ['l', Unprintable], [lambda n, *_: 's' in n]]))
@pytest.mark.parametrize('i2,fs2', enumerate([None, ['s'], ['l', Unprintable], [lambda n, *_: 's' in n]]))
def test_var_printers(check, i1, fs1, i2, fs2):
    check(fmt=Format(
        custom_var_printers=([(fs1, lambda v: None)] if fs1 else []) + ([(fs2, lambda v: 'var')] if fs2 else [])
    ))


@pytest.mark.parametrize('num_skipped_frames', [0, 1])
def test_cur_tb(tb_reg, num_skipped_frames):
    tb_reg(core.format_cur_tb(num_skipped_frames=num_skipped_frames, fmt=Format(skip_files_except='test_core')))

