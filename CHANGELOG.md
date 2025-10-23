# Changelog

## 2.2.1
- no formal deps shown by github
- supported python versions are [3.7 ... 3.14]
- more tests

## 2.2.0
- Fully compatible with >=2.0.4
- (BIG) Huge collections are printed faster, time depends only on `max_value_str_len`
- Add `hide`, `skip`, `show` as standard prints
- Variables like `password` and `token` are now hidden by default
- Added warning about secrets to readme, an example code to deal with it and a short essay
- Tested in python 3.13 and python 3.7
- More test cases and data types
- All objects without custom `__str__` or `__repr__` are printed with all attrs
- Standard backup tracebacks have this library stacks collapsed

## 2.1.1
- Fully compatible with >=2.0.4
- Add "tb" alias creation for lines like `import tb.a`

## 2.1.0
- Fully compatible with 2.0.4
- Add short names for frequently used things like `a` and `fmt`
- Add unified `activate_by_import` to be used both for Jupyter and regular Python
- Add relative ellipsis position for strings like `x=['some', ...long', 'list']`
- Add detailed object printout, useful for non-dataclass classes
- Add protection against acidental mistyping in format attributes
- Fixed some bugs, e.g.
    - cli not working in Python 3.12+
    - `default_format` being sometimes ignored

## 2.0.4
- ...much, to be filled...

## 2.0.3
- Fixed tests in Windows/Mac
- Removed `sys` from globals in the "main" mode

## 2.0.2
- Fixed globals when calling extrnally, i.e. in the "main" mode

## 2.0.0
- Some renames, no compatibility with previous versions
- Add `Format` and pack all style arguments inside it
- Add `before` and `after` instead of `num_context_lines`
- Add `skip-files-except` and `brief-files-except`
- Add warning on sensitive data
- Add colab badge
- Add a single `customized` example
- Add `custom_var_printers`
- Add past exceptions discovery
- Add current tb printing
- Add `format_*` functions to `core`
- Rename `*_tb` functions to `*_exc`
- Add `*_cur_tb*` methods

