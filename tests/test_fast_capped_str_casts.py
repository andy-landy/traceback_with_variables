import os
import time
from decimal import Decimal
from collections import deque, defaultdict
from pathlib import Path

import pytest

from traceback_with_variables.fast_capped_str_casts import (
    ToCappedStr,
    TokensInfo,
    fill_tokens,
    has_custom_str_or_repr,
    to_capped_str,
    to_big_tokens,
    tokens_to_big_tokens,
)

from tests.dummies import (
    A,
    D,
    DWithRepr,
    DWithStr,
    HasNoStr,
    HasStr,
    SuperDict,
    SuperList,
    SuperSet,
    Unprintable,
    f,
)
from tests.test_utils import (
    tb_reg,
    type_to_name,
)


def get_len(obj):
    try:
        return str(len(obj))
    except Exception:
        return 'na'


OBJS = [
    5,
    5.0,
    'five',
    # Decimal(5.5),
    True,
    False,
    list,
    HasStr,
    [1, 2, 3],
    [1],
    [],
    (1, 2, 3),
    (1,),
    tuple(),
    {1, 2, 3},
    {1},
    set(),
    {'k1': 'v1', 'a2': 'k2', 'a3': 'k3'},
    {'k1': 'v1'},
    {},
    HasStr(),
    HasNoStr(),
    A.B(11),
    A(11, 12),
    A([1, 2, 3], 4),
    D(11, 12),
    D([1, 2, 3], 4),
    # opened file
    # Path
    # ? todo more
    [1, 2.0, 'three', HasStr(), A([HasNoStr(), True, 4], {5: SuperSet([HasStr(), A(6, 7), None]), 8:-9})],
    SuperList([11, 12, 13]),
    SuperDict([('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]),
    Decimal('12.34'),
    defaultdict(str, [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')]),
    deque([11, 12, 13]),
    DWithRepr('v1'),
    DWithStr('v1'),
    open('./temp_out.txt', 'w', encoding='UTF-8'),
    Path('/some/path/to/file.txt'),
]
OBJ_IDS = [f'obj{oi:03}-{type_to_name(type(obj))}-{get_len(obj)}' for oi, obj in enumerate(OBJS)]

HUGE_OBJS = [
    list(range(1000, 1000000)),
    set(range(1000, 1000000)),
    {i: i + 10 for i in range(1000, 1000000)},
    D(list(range(1000)), list(range(1000000))),
]
HUGE_OBJ_IDS = [f'huge_{n}' for n in ['list', 'set', 'dict', 'D']]


def test_env():
    assert os.getenv('PYTHONHASHSEED') == '1'


def test_tokens_to_big_tokens():
    tokens1 = ['a', 'bc', '', 'def']
    assert list(tokens_to_big_tokens(tokens=tokens1, reverse=False, str_len_cap=-1)) == ['abcdef']
    assert list(tokens_to_big_tokens(tokens=tokens1, reverse=False, str_len_cap=0)) == ['', '']
    assert list(tokens_to_big_tokens(tokens=tokens1, reverse=False, str_len_cap=1)) == ['a', '']
    assert list(tokens_to_big_tokens(tokens=tokens1, reverse=False, str_len_cap=2)) == ['a', 'b']
    assert list(tokens_to_big_tokens(tokens=tokens1, reverse=False, str_len_cap=3)) == ['abc', '']
    assert list(tokens_to_big_tokens(tokens=tokens1, reverse=False, str_len_cap=4)) == ['abc', 'd']
    assert list(tokens_to_big_tokens(tokens=tokens1, reverse=False, str_len_cap=5)) == ['abc', 'de']
    assert list(tokens_to_big_tokens(tokens=tokens1, reverse=False, str_len_cap=6)) == ['abcdef']
    assert list(tokens_to_big_tokens(tokens=tokens1, reverse=False, str_len_cap=7)) == ['abcdef']
    
    tokens2 = ['def', '', 'bc', 'a']
    assert list(tokens_to_big_tokens(tokens=tokens2, reverse=True, str_len_cap=-1)) == ['abcdef']
    assert list(tokens_to_big_tokens(tokens=tokens2, reverse=True, str_len_cap=0)) == ['', '']
    assert list(tokens_to_big_tokens(tokens=tokens2, reverse=True, str_len_cap=1)) == ['f', '']
    assert list(tokens_to_big_tokens(tokens=tokens2, reverse=True, str_len_cap=2)) == ['ef', '']
    assert list(tokens_to_big_tokens(tokens=tokens2, reverse=True, str_len_cap=3)) == ['', 'def']
    assert list(tokens_to_big_tokens(tokens=tokens2, reverse=True, str_len_cap=4)) == ['c', 'def']
    assert list(tokens_to_big_tokens(tokens=tokens2, reverse=True, str_len_cap=5)) == ['', 'bcdef']
    assert list(tokens_to_big_tokens(tokens=tokens2, reverse=True, str_len_cap=6)) == ['abcdef']
    assert list(tokens_to_big_tokens(tokens=tokens2, reverse=True, str_len_cap=7)) == ['abcdef']

    tokens3 = []
    assert list(tokens_to_big_tokens(tokens=tokens3, reverse=False, str_len_cap=-1)) == ['']
    assert list(tokens_to_big_tokens(tokens=tokens3, reverse=False, str_len_cap=0)) == ['']
    assert list(tokens_to_big_tokens(tokens=tokens3, reverse=False, str_len_cap=1)) == ['']
    assert list(tokens_to_big_tokens(tokens=tokens3, reverse=True, str_len_cap=-1)) == ['']
    assert list(tokens_to_big_tokens(tokens=tokens3, reverse=True, str_len_cap=0)) == ['']
    assert list(tokens_to_big_tokens(tokens=tokens3, reverse=True, str_len_cap=1)) == ['']


@pytest.mark.parametrize('obj', OBJS, ids=OBJ_IDS)
def test_left_equals_right(obj, tb_reg):
    left_info = TokensInfo.create(-1)
    right_info = TokensInfo.create(-1)
    fill_tokens(obj=obj, info=left_info, reverse=False, obj_depth=-1)
    fill_tokens(obj=obj, info=right_info, reverse=True, obj_depth=-1)
    left_str = ''.join(left_info.tokens)
    assert left_str == ''.join(reversed(right_info.tokens))
    tb_reg(left_str)


def test_unprintable():
    with pytest.raises(ValueError):
        to_capped_str(obj=Unprintable(), len_cap=-1)
    with pytest.raises(ValueError):
        to_capped_str(obj=A(1, [2, Unprintable()]), len_cap=-1)


@pytest.mark.parametrize('obj', HUGE_OBJS, ids=HUGE_OBJ_IDS)
def test_speed(obj):
    if not os.getenv('PYTEST_RUN_PERF_TESTS'):
        return

    start_t_s = time.time()
    str(obj)
    long_dur_s = time.time() - start_t_s
    start_t_s = time.time()
    to_capped_str(obj=obj, len_cap=20)
    short_dur_s = time.time() - start_t_s
    assert long_dur_s > 100.0 * short_dur_s
    

@pytest.mark.parametrize('obj_depth', [-1, 0, 1, 2, 3])
def test_obj_depth(tb_reg, obj_depth):
    obj = [1, 2.0, 'three', HasStr(), A([HasNoStr(), True, 4], {5: SuperSet([HasStr(), A(6, 7), None]), 8:-9})]
    tb_reg(to_capped_str(obj=obj, len_cap=-1, obj_depth=obj_depth))


@pytest.mark.parametrize('len_cap', [3, 5, 10, 100], ids=['3', '5', '10', '100'])
@pytest.mark.parametrize('obj', OBJS, ids=OBJ_IDS)
def test_to_big_tokens(len_cap, obj, tb_reg):
    tb_reg(''.join(to_big_tokens(obj=obj, ellipsis='...', rel_ellipsis_pos=0.7, len_cap=len_cap, obj_depth=-1)), 'mid')
    tb_reg(''.join(to_big_tokens(obj=obj, ellipsis='...', rel_ellipsis_pos=0.0, len_cap=len_cap, obj_depth=-1)), 'left')
    tb_reg(''.join(to_big_tokens(obj=obj, ellipsis='...', rel_ellipsis_pos=1.0, len_cap=len_cap, obj_depth=-1)), 'right')


def test_has_custom_str_or_repr():
    assert has_custom_str_or_repr(D) == False
    assert has_custom_str_or_repr(DWithStr) == True
    assert has_custom_str_or_repr(DWithRepr) == True
    assert has_custom_str_or_repr(HasStr) == True
    assert has_custom_str_or_repr(HasNoStr) == False
    assert has_custom_str_or_repr(float) == True
    assert has_custom_str_or_repr(list) == True
    assert has_custom_str_or_repr(SuperList) == True


def test_to_capped_str_closure():
    closure = ToCappedStr(len_cap=7, rel_ellipsis_pos=0.5, ellipsis='...', obj_depth=-1)
    assert closure([1, 2, 3]) == '[1...3]'
