from traceback_with_variables import a

# or just
# import tb.a
# if you created the tb alias

# or
# from traceback_with_variables import activate_by_import
# if you prefer better names

n = 0
1/0





"""How to install in Colab etc."""

!pip install traceback-with-variables
# add this to use "tb" alias for the package
from tracaback_with_variables import create_tb_alias
create_tb_alias()
