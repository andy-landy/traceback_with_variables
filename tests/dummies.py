from dataclasses import dataclass
from typing import Any


@dataclass
class D:
    f1: Any
    f2: Any


@dataclass
class DWithRepr:
    f1: Any

    def __repr__(self):
        return f'DWithRepr-{self.f1}'


@dataclass
class DWithStr:
    f1: Any

    def __str__(self):
        return f'DWithStr-{self.f1}'


class Unprintable:
    def __repr__(self):
        raise ValueError("please don't print me")


class A:
    class B:
        def __init__(self, f3):
            self.f3 = f3

    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

    def __hash__(self):
        return hash((self.f1, self.f2))

    def __eq__(self, other):
        return type(self) == type(other) and self.f1 == other.f1 and self.f2 == other.f2


class SuperList(list):
    pass


class SuperDict(dict):
    pass


class SuperSet(set):
    def __iter__(self):
        return iter(sorted(super().__iter__(), key=lambda x: (type(x).__qualname__, hash(x))))


class HasNoStr:
    f1 = 'one'

    def __init__(self):
        self.f2 = 'two'
        self.f3 = 'three'

    def __hash__(self):
        return hash((self.f2, self.f3))

    def __eq__(self, other):
        return type(self) == type(other) and self.f2 == other.f2 and self.f3 == other.f3


class HasStr(HasNoStr):
    def __str__(self):
        return f'HasStr-with-f2-{self.f2}-f3-{self.f3}'
    

def f(n: int = 10001) -> int:
    s1 = f'short string with n: {n}'
    l1 = f'long string with 0..n: {", ".join(map(str, range(n)))}'
    us = [Unprintable(), Unprintable(), Unprintable()]

    if n % 10 == 0:
        return 1 // (n * 0)

    if True:
        if n % 2 == 0:
            return f(n - 1)
        else:
            return f(
                n

                - 1
            )