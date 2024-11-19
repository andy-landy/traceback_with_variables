# Changelog

## 2.1.1
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
- Some renames
- Add `Format` and pack all style arguments inside it
- Add `before` and `after` instead of `num_context_lines`
- Add `skip-files-except` and `brief-files-except`
- Add warning on sensitive data
- Add colab badge
- Add a single `customized` example
- Add `custom_var_printers`
- Add past exceptions discovery
- Add current tb printing
- Rm outer try block in `core`
- Add `format_*` functions to `core`
- Rename `*_tb` functions to `*_exc`
- Add `*_cur_tb*` methods

