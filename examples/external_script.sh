# if usually you called
  path/to/some_cmd --some-arg some-value
  # or
  path/to/some_script.py --some-arg some-value
  # or
  python3 path/to/some_script.py --some-arg some-value
  # or
  python3 -m some_module --some-arg some-value


# then you can upgrade the traceback like this:
  # script and it's args
  traceback-with-variables path/to/some_script.py --some-arg some-value ...

  # command known to be a script (e.g. 'pip') and it's args
  traceback-with-variables pip ...

  # a module (e.g. 'http.server') and it's args
  traceback-with-variables http.server ...


# help:
  traceback-with-variables --help


# synthwave
  traceback-with-variables --color-scheme synthwave ...


# more
  # with python -m
  python3 -m traceback_with_variables path/to/some_script.py --some-arg some-value

  # script and it's args, customized
  traceback-with-variables --max-value-str-len 100 --num-context-lines 3 path/to/some_script.py --some-arg some-value

  # command known to be a script (e.g. 'pip') and it's args, customized
  traceback-with-variables --max-value-str-len 100 --num-context-lines 3 some_cmd --some-arg some-value

  # a module (e.g. 'http.server') and it's args
  traceback-with-variables --max-value-str-len 100 module_name --some-arg some-value
