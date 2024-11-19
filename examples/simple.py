from traceback_with_variables import a  # , fmt
# or
from traceback_with_variables import activate_by_import  # , fmt
# or (if you added the "tb" alias)
import tb.a  


# fmt.max_value_str_len = 10000

def main():
    n = 0
    print(1 / n)


main()
