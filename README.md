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
    return wifth / height
      width = 300
      height = 0
builtins.ZeroDivisionError: division by zero
```


* output to `sys.stderr` (default) or any opened file (use `LoggerAsFile` to wrap a logger)
* limit messages size, set `max_value_str_len`
* all exceptions raised while printing out the traceback are caught and printed too

