from traceback_with_variables import print_cur_tb  # , format_cur_tb, iter_cur_tb_lines


def f(n):
    print_cur_tb()
    # cur_tb_str = format_cur_tb()
    # cur_tb_lines = list(iter_cur_tb_lines())

    return n + 1


def main():
    f(10)


main()
