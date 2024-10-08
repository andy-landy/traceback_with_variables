class Unprintable:
    def __repr__(self):
        raise ValueError("please don't print me")


class A:
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2


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