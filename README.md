```
def example(h1, w1, h2, w2):
    with rich_traceback():
        get_avg_ratio([h1, w1], [h2, w2])
```

```
RichTraceback (most recent call last):
  File "./test.py", line 25, in example
    get_avg_ratio([h1, w1], [h2, w2])
      h1 = 300
      w1 = 200
      h1 = 300
      w1 = 0
  File "./test.py", line 16, in get_avg_ratio
    ratios = [get_ratio(w, h) for w, h in [size1, size2]]
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

What if you want to log it silently?

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


* output to `sys.stderr` (default) or any opened file (use `LoggerAsFile` to wrap a logger)
* limit messages size, set `max_value_str_len`
* all exceptions raised while printing out the traceback are caught and printed too

