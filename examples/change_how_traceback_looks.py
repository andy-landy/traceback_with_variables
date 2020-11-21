from traceback_with_variables import override_print_tb


def main():
    override_print_tb(
        # ipython=True  # for Jupyter or IPython
    )

    n = 0
    print(1 / n)


main()
