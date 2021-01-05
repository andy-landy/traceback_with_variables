from traceback_with_variables import iter_exc_lines


def main():
    try:
        n = 0
        print(1 / n)

    except Exception as e:
        lines = list(iter_exc_lines(e))

        # requests.post('http://myreport.mysite.com/report', data={'lines': lines})


main()
