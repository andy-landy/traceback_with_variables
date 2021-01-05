>>> from traceback_with_variables import print_exc

>>> def f(n):
....  return 1 / n
....

>>> f(0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in f
ZeroDivisionError: division by zero

>>> print_exc()

>>> # you might want to import activate_[in_ipython]by_import to automate this step