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
  traceback-with-varaibles path/to/some_script.py --some-arg some-value ...

  # command known to be a script (e.g. 'pip') and it's args
  traceback-with-varaibles pip ...

  # a module (e.g. 'http.server') and it's args
  traceback-with-varaibles http.server ...


# help:
  traceback-with-variables --help


# synthwave
  traceback_with_variables --color-scheme synthwave ...


# more
  # with python -m
  python3 -m traceback_with_variables path/to/some_script.py --some-arg some-value

  # script and it's args, customized
  traceback-with-varaibles --max-value-str-len 100 --num-context-lines 3 path/to/some_script.py --some-arg some-value

  # command known to be a script (e.g. 'pip') and it's args, customized
  traceback-with-varaibles --max-value-str-len 100 --num-context-lines 3 some_cmd --some-arg some-value

  # a module (e.g. 'http.server') and it's args
  traceback-with-varaibles --max-value-str-len 100 module_name --some-arg some-value