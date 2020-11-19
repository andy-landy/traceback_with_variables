from traceback_with_variables import iter_tb_lines


@app.errorhandler(Exception)
def handle_exception(e):
    for line in iter_tb_lines(e):
        app.logger.error(line)

    return 'Server Error', 500  # prod
    return '\n'.join(iter_tb_lines(e)), 500  # debug mode


