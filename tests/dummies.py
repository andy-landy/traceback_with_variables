class Unprintable:
    def __repr__(self):
        raise ValueError("please don't print me")


def f(n: int) -> int:
    s1 = 'short string with n: {}'.format(n)
    l1 = 'long string with 0..n: {}'.format(', '.join(map(str, range(n))))
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