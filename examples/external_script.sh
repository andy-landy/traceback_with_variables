# if normally you called
  some_cmd ...its args...
  # or
  path/to/some_script.py ...its args...
  # or
  python3 path/to/some_script.py ...its args...
  # or
  python3 -m some_module ...its args...


# then your calls become:
  # command known to be a script (e.g. 'pip') and it's args
  traceback-with-variables some_cmd ...its args...
  
  # script and it's args
  traceback-with-variables path/to/some_script.py ...its args...

  # a module (e.g. 'http.server') and it's args
  traceback-with-variables some_module ...its args...


# help:
  traceback-with-variables --help


# more
  # customizing tracebacks
  traceback-with-variables --max-value-str-len 100 --before 3 --after 1 path/to/some_script.py ...its args...

  # print less blocks
  traceback-with-variables --skip-files-except my_porject site --brief-files-except my_project

  # no globals
  traceback-with-variables --no-globals ...
  
  # synthwave+
  traceback-with-variables --color-scheme synthwave ...
  traceback-with-variables --color-scheme nice ...
  
  # runnig with `python -m`
  python3 -m traceback_with_variables path/to/some_script.py ...its args...

