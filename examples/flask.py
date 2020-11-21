from traceback_with_variables import iter_tb_lines


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error('\n'.join(iter_tb_lines(e)))

    return 'Server Error', 500  # for prod
    return '\n'.join(iter_tb_lines(e)), 500  # for debug mode


