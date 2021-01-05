from traceback_with_variables import format_exc


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(format_exc(e))

    return 'Server Error', 500  # for a simple prod server
    return format_exc(e), 500  # for a debug server
