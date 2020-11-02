from traceback_with_variables import prints_tb


@prints_tb(
    num_context_lines=3,
    max_value_str_len=100,
    max_exc_str_len=1000,
    ellipsis_='...',
)
def f(n):
    print(1 / n)


def main():
    f(0)


main()
