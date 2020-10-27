## Add variable values to the standard traceback.

### 
###
###

#### Tired of putting all your variables in debug exception messages? Just stop it. Go clean your code.

```diff
+ from traceback_with_variables import traceback_with_variables

  def main():
      sizes_str = sys.argv[1]
      h1, w1, h2, w2 = map(int, sizes_str.split())
-     try:
+     with traceback_with_variables():
          return get_avg_ratio([h1, w1], [h2, w2])
-     except:
-         logger.error(f'something happened :(, variables = {variables()[:1000]}')
-         raise
-         # or
-         raise MyToolException(f'something happened :(, variables = {variables()[:1000]}')
          
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
Traceback with variables (most recent call last):
  File "./temp.py", line 7, in main
    return get_avg_ratio([h1, w1], [h2, w2])
      sizes_str = '300 200 300 0'
      h1 = 300
      w1 = 200
      h2 = 300
      w2 = 0
  File "./temp.py", line 10, in get_avg_ratio
    return mean([get_ratio(h, w) for h, w in [size1, size2]])
      size1 = [300, 200]
      size2 = [300, 0]
  File "./temp.py", line 10, in <listcomp>
    return mean([get_ratio(h, w) for h, w in [size1, size2]])
      .0 = <tuple_iterator object at 0x7ff61e35b820>
      h = 300
      w = 0
  File "./temp.py", line 13, in get_ratio
    return height / width
      height = 300
      width = 0
builtins.ZeroDivisionError: division by zero
```

#### What if you want to log it silently?

```python
def main():
    ...
    with traceback_with_variables(
        file_=LoggerAsFile(logging.getLogger('main')),
        reraise=False
    ):
        ...
```

```
2020-03-30 18:24:31 main ERROR Traceback with variables (most recent call last):
2020-03-30 18:24:31 main ERROR   File "./temp.py", line 7, in main
2020-03-30 18:24:31 main ERROR     return get_avg_ratio([h1, w1], [h2, w2])
2020-03-30 18:24:31 main ERROR       sizes_str = '300 200 300 0'
2020-03-30 18:24:31 main ERROR       h1 = 300
2020-03-30 18:24:31 main ERROR       w1 = 200
2020-03-30 18:24:31 main ERROR       h2 = 300
2020-03-30 18:24:31 main ERROR       w2 = 0
2020-03-30 18:24:31 main ERROR   File "./temp.py", line 10, in get_avg_ratio
2020-03-30 18:24:31 main ERROR     return mean([get_ratio(h, w) for h, w in [size1, size2]])
2020-03-30 18:24:31 main ERROR       size1 = [300, 200]
2020-03-30 18:24:31 main ERROR       size2 = [300, 0]
2020-03-30 18:24:31 main ERROR   File "./temp.py", line 10, in <listcomp>
2020-03-30 18:24:31 main ERROR     return mean([get_ratio(h, w) for h, w in [size1, size2]])
2020-03-30 18:24:31 main ERROR       .0 = <tuple_iterator object at 0x7ff412acb820>
2020-03-30 18:24:31 main ERROR       h = 300
2020-03-30 18:24:31 main ERROR       w = 0
2020-03-30 18:24:31 main ERROR   File "./temp.py", line 13, in get_ratio
2020-03-30 18:24:31 main ERROR     return height / width
2020-03-30 18:24:31 main ERROR       height = 300
2020-03-30 18:24:31 main ERROR       width = 0
2020-03-30 18:24:31 main ERROR builtins.ZeroDivisionError: division by zero
```

#### Also you can:

* output to `sys.stderr` (default) or any opened file (use `LoggerAsFile` to wrap a logger)
* limit messages size, set `max_value_str_len`
* all exceptions raised while printing out the traceback are caught and printed too

#### Rationale: free your exceptions of unnecessary information load:

```python
def make_a_cake(sugar, eggs, milk, flour, salt, water):
    is_sweet = sugar > salt
    is_vegan = not (eggs or milk)
    is_huge = (sugar + eggs + milk + flour + salt + water > 10000)
    if not (is_sweet or is_vegan or is_huge):
        raise ValueError('This is unacceptable, guess why!')
    ...
```

#### Rationale: stop this tedious practice in production:

1. Notice some exception in a production service.
2. Add more printouts, logging, and exception messages.
3. Rerun the service.
4. Wait till (hopefully) the bug repeats.
5. Examine the printouts and possibly add some more info (then go back to step 2).
6. Erase all recently added printouts, logging and exception messages.
7. Go back to step 1 once bugs appear.

#### Installation (simple checkout)

```
git clone https://github.com/andy-landy/traceback_with_variables.git
cp -r traceback_with_variables/traceback_with_variables path/to/your/libs
rm -r traceback_with_variables
```
