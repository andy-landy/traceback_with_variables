# Changelog

## 2.0.3
- Fixed tests in Windows/Mac
- Removed `sys` from globals in the "main" mode

## 2.0.2
- Fixed globals when calling extrnally, i.e. in the "main" mode

## 2.0.0
- Some renames
- Add `Format` and pack all style arguments inside it
- Add `before` and `after` instead of `num_context_lines`
- Add `README.tmpl`
- Add `print_tb()` to use out of try/except
- Add `skip-files-except` and `brief-files-except`
- Add warning on sensitive data
- Add colab badge
- Make a single `customized` example
- Add `custom_var_printers`
- Add past exceptions discovery
- Add current tb printing
- Rm outer try block in `core`
- Add `format_*` functions to `core`
- Rename `*_tb` functions to `*_exc`
- Add `*_cur_tb*` methods
- Add contributing md

