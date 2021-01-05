!pip install traceback_with_variables
from traceback_with_variables import global_print_exc_in_ipython


global_print_exc_in_ipython()


def main():
    n = 0
    print(1 / n)


main()
