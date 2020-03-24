## Add the variable values to the standard traceback.

### 
###
###

#### Tired of putting all your variables in debug exception messages? Just stop it. Go clean your code.

```diff
  def example(h1, w1, h2, w2):
-     try:
+     with rich_traceback():
          return get_avg_ratio([h1, w1], [h2, w2])
-     except:
-         logger.error(f'something happened :(, h1 = {h1}, w1 = {w1}, h2 = {h2}, w2 = {w2}')
-         raise
-         # or
-         raise MyToolException(f'something happened :(, h1 = {h1}, w1 = {w1}, h2 = {h2}, w2 = {w2}')
          
  def get_avg_ratio(size1, size2):
-     try:
          return mean(get_ratio(h, w) for h, w in [size1, size2])
-     except:
-         logger.error(f'something happened :(, size1 = {size1}, size2 = {size2}')
-         raise
-         # or
-         raise MyToolException(f'something happened :(, size1 = {size1}, size2 = {size2}')

  def get_ratio(height, width):
-     try:
          return height / width
-     except:
-         logger.error(f'something happened :(, width = {width}, height = {height}')
-         raise
-         # or
-         raise MyToolException(f'something happened :(, width = {width}, height = {height}')
```

```
RichTraceback (most recent call last):
  File "./test.py", line 25, in example
    return get_avg_ratio([h1, w1], [h2, w2])
      h1 = 300
      w1 = 200
      h2 = 300
      w2 = 0
  File "./test.py", line 16, in get_avg_ratio
    return mean(get_ratio(h, w) for h, w in [size1, size2])
      size1 = [300, 200]
      size2 = [300, 0]
      w = 300
      h = 0
  File "./test.py", line 10, in get_ratio
    return width / height
      width = 300
      height = 0
builtins.ZeroDivisionError: division by zero
```

#### What if you want to log it silently?

```
def example(h1, w1, h2, w2):
    with rich_traceback(file_=LoggerAsFile(logging.getLogger('main')), reraise=False):
        get_avg_ratio([h1, w1], [h2, w2])
```

```
2020-03-30 18:24:31 main ERROR RichTraceback (most recent call last):
2020-03-30 18:24:31 main ERROR   File "./test.py", line 25, in example
2020-03-30 18:24:31 main ERROR     get_avg_ratio([h1, w1], [h2, w2])
2020-03-30 18:24:31 main ERROR       h1 = 300
2020-03-30 18:24:31 main ERROR       w1 = 200
2020-03-30 18:24:31 main ERROR       h1 = 300
2020-03-30 18:24:31 main ERROR       w1 = 0
2020-03-30 18:24:31 main ERROR   File "./test.py", line 16, in get_avg_ratio
2020-03-30 18:24:31 main ERROR     ratios = [get_ratio(w, h) for w, h in [size1, size2]]
2020-03-30 18:24:31 main ERROR       size1 = [300, 200]
2020-03-30 18:24:31 main ERROR       size2 = [300, 0]
2020-03-30 18:24:31 main ERROR       w = 300
2020-03-30 18:24:31 main ERROR       h = 0
2020-03-30 18:24:31 main ERROR   File "./test.py", line 10, in get_ratio
2020-03-30 18:24:31 main ERROR     return width / height
2020-03-30 18:24:31 main ERROR       width = 300
2020-03-30 18:24:31 main ERROR       height = 0
2020-03-30 18:24:31 main ERROR builtins.ZeroDivisionError: division by zero
```

#### Also you can:

* output to `sys.stderr` (default) or any opened file (use `LoggerAsFile` to wrap a logger)
* limit messages size, set `max_value_str_len`
* all exceptions raised while printing out the traceback are caught and printed too

#### Mission: free your exceptions of unnecesseary information load:

```
def make_a_cake(sugar, eggs, milk, flour, salt, water, chief):
    is_sweet = sugar > salt
    is_vegan = not (eggs or milk)
    is_huge = (sugar + eggs + milk + flour + salt + water > 10000)
    if not (is_sweet and chief.can_make_huge() and chief.can_make_vegan(is_vegan)):
        raise ValueError('This is unacceptable!')
    ...
```

#### Mission: stop this tedious practice in production:

1. Notice some exception in a production service.
2. Add more printouts, logging, and exception messages.
3. Rerun the service.
4. Wait till (hopefully) the bug repeats.
5. Examine the printouts and possibly add some more info (then go back to step 2).
6. Erase all recently added printouts, logging and exception messages.
7. Go back to step 1 once bugs appear.
