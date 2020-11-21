from traceback_with_variables import override_print_tb, ColorSchemes


def main():
    override_print_tb(
        num_context_lines=3,
        max_value_str_len=100,
        max_exc_str_len=1000,
        ellipsis_='...',
        activate_by_env_var='PY_PRINT_VARS',
        deactivate_by_env_var='PY_DONT_PRINT_VARS',
        color_scheme=ColorSchemes.synthwave,
        # ipython=True  # for Jupyter or IPython
    )

    n = 0
    print(1 / n)


main()
