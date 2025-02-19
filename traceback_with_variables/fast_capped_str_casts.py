import dataclasses
import reprlib
import sys
from decimal import Decimal
from typing import List, Iterator, Iterable, Any, Type


@dataclasses.dataclass
class TokensInfo:
    class CapMet(Exception):
        pass

    str_len_cap: int
    tokens: List[str]
    str_len: int

    @classmethod
    def create(cls, str_len_cap: int) -> 'TokenInfo':  # noqa: F821
        return cls(str_len_cap=str_len_cap, tokens=[], str_len=0)

    def add_token(self, token: str) -> None:
        self.tokens.append(token)
        self.str_len += len(token)
        if self.str_len_cap >= 0 and self.str_len > self.str_len_cap:
            raise TokensInfo.CapMet()

    def add_tokens(self, tokens: Iterable[str]) -> None:
        for token in tokens:
            self.add_token(token)


def tokens_to_big_tokens(tokens: List[str], str_len_cap: int, reverse: bool) -> Iterator[str]:
    if str_len_cap < 0 or str_len_cap >= sum(len(token) for token in tokens):
        yield ''.join(reversed(tokens) if reverse else tokens)
        return

    sum_token_len = 0
    for num_full_tokens, token in enumerate(tokens):
        if sum_token_len + len(token) > str_len_cap:
            break
        sum_token_len += len(token)

    if reverse:
        yield token[sum_token_len - str_len_cap:] if sum_token_len < str_len_cap else ''
        yield ''.join(reversed(tokens[:num_full_tokens]))
    else:
        yield ''.join(tokens[:num_full_tokens])
        yield token[:str_len_cap - sum_token_len]


DATACLASSES_FILENAME = dataclasses.is_dataclass.__code__.co_filename
REPRLIB_FILENAME = reprlib.recursive_repr.__code__.co_filename


def has_custom_str_or_repr(type_: Type) -> bool:
    if type_.__str__ != object.__str__:
        return True

    if type_.__repr__ == object.__repr__:
        return False

    if dataclasses.is_dataclass(type_):
        if sys.version_info >= (3, 13):
            return type_.__repr__.__code__.co_filename != REPRLIB_FILENAME
        elif sys.version_info >= (3, 10):
            return type_.__repr__.__code__.co_filename != DATACLASSES_FILENAME
        else:
            return type_.__repr__.__qualname__ != '__create_fn__.<locals>.__repr__'

    return True


_MODULES_TO_HIDE = {'builtins', '__main__'}


def type_to_str(type_: Type) -> str:
    name = type_.__qualname__
    module = type_.__module__

    return f'{module}.{name}' if module not in _MODULES_TO_HIDE else name


def fill_tokens(obj: Any, info: TokensInfo, reverse: bool, obj_depth: int) -> None:
    type_ = type(obj)

    if isinstance(obj, str):
        info.add_tokens(["'", obj, "'"])

    elif obj is None or isinstance(obj, (int, bool, float, Decimal)):
        info.add_token(str(obj))

    elif isinstance(obj, type):
        info.add_token(type_to_str(obj))

    elif isinstance(obj, (list, tuple, set)):
        if isinstance(obj, list):
            open_token, close_token = '[', ']'
        elif isinstance(obj, tuple):
            open_token, close_token = '(', ')'
        else:
            if len(obj) == 0:
                info.add_token(type_to_str(type_) + '()')  # i.e. 'set()', not '{}'
                return
            open_token, close_token = '{', '}'
        type_token = type_to_str(type_) if type_ not in {list, tuple, set} else ''

        if type_token and not reverse:
            info.add_token(type_token)
        info.add_token(close_token if reverse else open_token)
        needs_comma = False
        for el in (reversed(list(obj) if isinstance(obj, set) else obj) if reverse else obj):
            if needs_comma:
                info.add_token(', ')
            fill_tokens(obj=el, info=info, reverse=reverse, obj_depth=obj_depth)
            needs_comma = True
        info.add_token(open_token if reverse else close_token)
        if type_token and reverse:
            info.add_token(type_token)

    elif isinstance(obj, dict):
        open_token, close_token = '{', '}'
        type_token = type_to_str(type_) if type_ != dict else ''
        if type_token and not reverse:
            info.add_token(type_token)

        info.add_token(close_token if reverse else open_token)
        needs_comma = False
        for key, value in (reversed(obj.items()) if reverse else obj.items()):
            if needs_comma:
                info.add_token(', ')
            for step in range(2, -1, -1) if reverse else range(3):
                if step == 0:
                    fill_tokens(obj=key, info=info, reverse=reverse, obj_depth=obj_depth)
                elif step == 1:
                    info.add_token(': ')
                else:
                    fill_tokens(obj=value, info=info, reverse=reverse, obj_depth=obj_depth)
            needs_comma = True
        info.add_token(open_token if reverse else close_token)
        if type_token and reverse:
            info.add_token(type_token)

    else:
        if has_custom_str_or_repr(type_):
            info.add_token(str(obj))
        else:
            open_tokens = [type_to_str(type_), '(']
            close_tokens = [')']
            info.add_tokens(reversed(close_tokens) if reverse else open_tokens)
            if obj_depth == 0:
                info.add_token('-')
            else:
                type_attrs = set(dir(type_))
                own_attrs = [attr for attr in dir(obj) if not ((attr in type_attrs) or attr.startswith('_'))]
                needs_comma = False
                for attr in reversed(own_attrs) if reverse else own_attrs:
                    if needs_comma:
                        info.add_token(', ')

                    for step in range(2, -1, -1) if reverse else range(3):
                        if step == 0:
                            info.add_token(attr)
                        elif step == 1:
                            info.add_token('=')
                        else:
                            fill_tokens(obj=getattr(obj, attr), info=info, reverse=reverse, obj_depth=obj_depth - 1)

                    needs_comma = True
            info.add_tokens(reversed(open_tokens) if reverse else close_tokens)


def to_big_tokens(obj: Any, len_cap: int, rel_ellipsis_pos: float, ellipsis: str, obj_depth: int) -> Iterator[str]:
    left_info = TokensInfo.create(str_len_cap=len_cap)
    try:
        fill_tokens(obj=obj, info=left_info, reverse=False, obj_depth=obj_depth)

    except TokensInfo.CapMet:
        new_len_cap = max(0, len_cap - len(ellipsis))
        left_len_cap = max(0, min(new_len_cap, int(new_len_cap * rel_ellipsis_pos)))
        right_info = TokensInfo.create(str_len_cap=new_len_cap - left_len_cap)
        try:
            fill_tokens(obj=obj, info=right_info, reverse=True, obj_depth=obj_depth)
        except TokensInfo.CapMet:
            pass
        yield from tokens_to_big_tokens(tokens=left_info.tokens, reverse=False, str_len_cap=left_len_cap)
        yield ellipsis
        yield from tokens_to_big_tokens(tokens=right_info.tokens, reverse=True, str_len_cap=right_info.str_len_cap)
        return

    yield ''.join(left_info.tokens)


def to_capped_str(obj: Any, len_cap: int, rel_ellipsis_pos: float = 1.0, ellipsis: str = '...', obj_depth: int = -1):
    return ''.join(to_big_tokens(
        obj=obj,
        len_cap=len_cap,
        rel_ellipsis_pos=rel_ellipsis_pos,
        ellipsis=ellipsis,
        obj_depth=obj_depth,
    ))


@dataclasses.dataclass
class ToCappedStr:
    len_cap: int
    rel_ellipsis_pos: float = 1.01
    ellipsis: str = '...'
    obj_depth: int = -1

    def __call__(self, obj: Any) -> str:
        return to_capped_str(
            obj=obj,
            len_cap=self.len_cap,
            rel_ellipsis_pos=self.rel_ellipsis_pos, ellipsis=self.ellipsis,
            obj_depth=self.obj_depth,
        )
