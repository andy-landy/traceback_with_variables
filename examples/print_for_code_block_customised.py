from traceback_with_variables import printing_tb


def f(n):
    print(1 / n)


def main():
    with printing_tb(
        num_context_lines=3,
        max_value_str_len=100,
        max_exc_str_len=1000,
        ellipsis_='...',
        skip_cur_frame=True,  # e.g. no info about 'x'
        reraise=False,  # i.e. program won't fail, exceptions stay inside
    ):
        x = 1
        f(x - 1)


main()
