from traceback_with_variables import override_print_tb


def main():
    override_print_tb()

    n = 0
    print(1 / n)


main()
