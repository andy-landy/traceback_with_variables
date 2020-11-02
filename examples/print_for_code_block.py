from traceback_with_variables import printing_tb


def f(n):
    print(1 / n)


def main():
    with printing_tb():
        x = 1
        f(x - 1)


main()
