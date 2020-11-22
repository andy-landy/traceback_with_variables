from traceback_with_variables import prints_exc


@prints_exc
def f(n):
    print(1 / n)


def main():
    f(0)


main()
