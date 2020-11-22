from traceback_with_variables import printing_exc


def f(n):
    print(1 / n)


def main():
    with printing_exc():
        x = 1
        f(x - 1)


main()
