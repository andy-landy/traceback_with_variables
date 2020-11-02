from traceback_with_variables import prints_tb


@prints_tb
def f(n):
    print(1 / n)


def main():
    f(0)


main()
