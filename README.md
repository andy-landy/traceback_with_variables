![Example](https://raw.githubusercontent.com/andy-landy/traceback_with_variables/master/header.png)

<h2 align="center">Python Traceback (Error Message) Printing Variables</h2>
<p align="center">Very simple to use, but versatile when needed. Try for debug and keep for production.</p>

<p align="center">
<a href="https://github.com/andy-landy/traceback_with_variables/actions"><img alt="Actions Status" src="https://github.com/andy-landy/traceback_with_variables/workflows/Tests/badge.svg"></a>
<a href="https://codecov.io/gh/andy-landy/traceback_with_variables"><img alt="Codecov" src="https://codecov.io/gh/andy-landy/traceback_with_variables/branch/master/graph/badge.svg"></a>
<a href="https://lgtm.com/projects/g/andy-landy/traceback_with_variables/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/andy-landy/traceback_with_variables.svg"/></a>
<a href="https://github.com/andy-landy/traceback_with_variables/blob/master/LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/andy-landy/traceback_with_variables?color=informational"></a>
<a href="https://pypi.org/project/traceback_with_variables/"><img alt="PyPI" src="https://img.shields.io/pypi/v/traceback_with_variables"></a>
<a href="https://anaconda.org/conda-forge/traceback-with-variables"><img src="https://img.shields.io/conda/vn/conda-forge/traceback-with-variables"></a>
<a href="https://pypi.org/project/traceback_with_variables/"><img alt="PyPI" src="https://img.shields.io/badge/python-3.5+-blue.svg"></a>
<a href="https://superuser.com/questions/413073/windows-console-with-ansi-colors-handling"><img title="windows, mac, linux etc." alt="Platform" src="https://img.shields.io/badge/platform-all-blue.svg"></a>
<a href="https://github.com/andy-landy/traceback_with_variables/blob/master/traceback_with_variables/override.py#L9"><img title="type hints everywhere" alt="Annotations coverage" src="https://img.shields.io/badge/type--hints-100%25-blueviolet.svg"></a>
<a href="https://github.com/andy-landy/traceback_with_variables/blob/master/traceback_with_variables/override.py#L8"><img title="no obscure objects, only transparent functions and data classes" alt="No-OOP" src="https://img.shields.io/badge/no OOP-100%25-blueviolet.svg"></a>
<a href="https://github.com/andy-landy/traceback_with_variables/blob/master/setup.py"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-0-blueviolet.svg"></a>
<a href="https://gitter.im/andy-landy/traceback-with-variables"><img alt="Gitter" src="https://img.shields.io/gitter/room/andy-landy/traceback-with-variables?color=blueviolet"></a>
<!--
<a href="https://pepy.tech/project/traceback_with_variables"><img alt="pip Downloads" src="https://static.pepy.tech/personalized-badge/traceback-with-variables?period=total&units=none&left_color=grey&right_color=orange&left_text=pip downloads"></a>
<a href="https://anaconda.org/conda-forge/traceback_with_variables/"><img alt="conda-forge Downloads" src="https://img.shields.io/conda/dn/conda-forge/traceback-with-variables?color=orange&label=conda%20downloads"></a>
-->
</p>
<br/>

> “It is useless work that darkens the heart.” 
> <em>– Ursula K. Le Guin</em>

Tired of useless job of putting all your variables into debug exception messages? Just stop it. 
Automate it and clean your code. Once and for all.

---

_Contents:_ **[Installation](#installation)** | **[🚀 Quick Start](#-quick-start)**
| **[Colors](#colors)**
| **[How does it save my time?](#how-does-it-save-my-time)** | 
**[Examples and recipes](#examples-and-recipes)** | **[Reference](#reference)**
| **[FAQ](#faq)**

---

> :warning: **This module is actively updated and has a substantial list of features to add this week**: so any proposal or advice or warning is very welcome and will be taken into account of course. When I started it I wanted to make a tool meeting all standard use cases. I think in this particular domain this is rather achievable, so I'll try. Note `next_version` branch also. Have fun!

---

### Installation

```
pip install traceback-with-variables
```
```
conda install -c conda-forge traceback-with-variables
```

### 🚀 Quick Start

Using without code editing, <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/external_script.sh">running your script/command/module</a>:
```
traceback-with-variables ...script/tool/module with arguments...
```

<a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/simple.py">Simplest usage in regular Python</a>, for the whole program:
```python
    from traceback_with_variables import activate_by_import
```

<a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/simple_jupyter.py">Simplest usage in Jupiter or IPython</a>, for the whole program:
```python
    from traceback_with_variables import activate_in_ipython_by_import
```


<a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/print_for_function.py">Decorator</a>, for a single function:
```python
    @prints_tb
    # def main(): or def some_func(...):
```

<a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/print_for_code_block.py">Context</a>, for a single code block:
```python
    with printing_tb():
```

<a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/work_with_traceback_lines.py">Work with traceback lines</a> in a custom manner:
```python
    return '\n'.join(iter_tb_lines(e))
```

Using a logger [<a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/log_for_function.py">with a decorator</a>, <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/log_for_code_block.py">with a context</a>]:
```python
    with printing_tb(file_=LoggerAsFile(logger)):
    # or
    @prints_tb(file_=LoggerAsFile(logger)): 
```

### Colors

![Example](https://raw.githubusercontent.com/andy-landy/traceback_with_variables/master/color_schemes.png)


### How does it save my time?

* Turn a code totally covered by debug formatting from this:

    ```diff
      def main():
          sizes_str = sys.argv[1]
          h1, w1, h2, w2 = map(int, sizes_str.split())
    -     try:
              return get_avg_ratio([h1, w1], [h2, w2])
    -     except:
    -         logger.error(f'something happened :(, variables = {locals()[:1000]}')
    -         raise
    -         # or
    -         raise MyToolException(f'something happened :(, variables = {locals()[:1000]}')
              
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
    into this (zero debug code):
    
    ```diff
    + from traceback_with_variables import activate_by_import
    
      def main():
          sizes_str = sys.argv[1]
          h1, w1, h2, w2 = map(int, sizes_str.split())
          return get_avg_ratio([h1, w1], [h2, w2])
              
      def get_avg_ratio(size1, size2):
          return mean(get_ratio(h, w) for h, w in [size1, size2])
    
      def get_ratio(height, width):
          return height / width
    ```
    
    And obtain total debug info spending 0 lines of code:
    
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

* Automate your logging too:
    
    ```python
    logger = logging.getLogger('main')
    
    def main():
        ...
        with printing_tb(file_=LoggerAsFile(logger))
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

* Free your exceptions of unnecessary information load:
    
    ```python
    def make_a_cake(sugar, eggs, milk, flour, salt, water):
        is_sweet = sugar > salt
        is_vegan = not (eggs or milk)
        is_huge = (sugar + eggs + milk + flour + salt + water > 10000)
        if not (is_sweet or is_vegan or is_huge):
            raise ValueError('This is unacceptable, guess why!')
        ...
    ```

* — Should I use it after debugging is over, i.e. *in production*?

    Yes, of course! That way it might save you even more time. (watch out if your variables have personal data, passwords etc. Filters with be introduced in next versions very soon)

<br/>

* Stop this tedious practice in production:
   
     step 1: Notice some exception in a production service. \
     step 2: Add more printouts, logging, and exception messages. \
     step 3: Rerun the service. \
     step 4: Wait till (hopefully) the bug repeats. \
     step 5: Examine the printouts and possibly add some more info (then go back to step 2). \
     step 6: Erase all recently added printouts, logging and exception messages. \
     step 7: Go back to step 1 once bugs appear.
     

### Examples and recipes

* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/external_script.sh">run python code without changes</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/simple.py">simple usage</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/simple_jupyter.py">simple usage in Jupyter or IPython</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/change_how_traceback_looks.py">a bit more controlled usage</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/change_how_traceback_looks_customised.py">a bit more controlled usage, customised</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/print_for_function.py">working with a function</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/print_for_function_customised.py">working with a function, customised</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/log_for_function.py">working with a function, logging</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/print_for_code_block.py">working with a code block</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/print_for_code_block_customised.py">working with a code block, customised</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/log_for_code_block.py">working with a code block, logging</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/work_with_traceback_lines.py">get traceback lines for custom things</a>
* <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/examples/flask.py">using with `flask`</a>

### Reference

#### All functions have output customization
* `max_value_str_len` max length of each variable string, -1 to disable, default=1000
* `max_exc_str_len` max length of exception, should variable print fail, -1 to disable, default=10000
* `num_context_lines` number of lines around the target code line to print, default=1
* `ellipsis_` string to denote long strings truncation, default=`...`
* `file_` where to print exception, a file or a wrapped logger, default=`sys.stderr` i.e. usual printing to console
* `color_scheme` one of <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/traceback_with_variables/color.py">`ColorSchemes`</a>: `.auto`, `.none` , `.common`, `.nice`, `.synthwave` 

---

#### <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/traceback_with_variables/activate_by_import.py">`activate_by_import`</a>
Just import it. No arguments, for real quick use in regular Python.
```python
from traceback_with_variables import activate_by_import
```

---

#### <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/traceback_with_variables/activate_in_ipython_by_import.py">`activate_in_ipython_by_import`</a>
Just import it. No arguments, for real quick use in Jupyter or IPython.
```python
from traceback_with_variables import activate_in_ipython_by_import
```

---

#### <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/traceback_with_variables/override.py">`override_print_tb`</a>
Call once in the beginning of your program, to change how traceback after an uncaught exception looks.
```python
def main():
    override_print_tb(...)
```

---

#### <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/traceback_with_variables/print.py">`prints_tb`</a>
Function decorator, used for logging or simple printing of scoped tracebacks with variables. I.e. traceback is shorter as it includes only frames inside the function call. Program exiting due to unhandled exception still prints a usual traceback.
```python
@prints_tb
def f(...):

@prints_tb(...)
def f(...):
```

---

#### <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/traceback_with_variables/print.py">`printing_tb`</a>
Context manager (i.e. `with ...`), used for logging or simple printing of scoped tracebacks with variables. I.e. traceback is shorter as it includes only frames inside the `with` scope. Program exiting due to unhandled exception still prints a usual traceback.
```python
with printing_tb(...):
```

---

#### <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/traceback_with_variables/print.py">`LoggerAsFile`</a>
A logger-to-file wrapper, to pass a logger to print tools as a file.

---

#### <a href="https://github.com/andy-landy/traceback_with_variables/tree/master/traceback_with_variables/core.py">`iter_tb_lines`</a>
Iterates the lines, which are usually printed one-by-one in terminal.

---

### FAQ

* In Windows console crash messages have no colors. 

    The default Windows console/terminal cannot print [so called *ansi*] colors, but this is 
    <a href="https://superuser.com/questions/413073/windows-console-with-ansi-colors-handling">fixable</a>
    , especially with modern Windows versions. Therefore colors are disabled by default,
    but you can enable them and check if it works in your case.
    You can force enable colors by passing `--color-scheme common` (for complete list of colors pass `--help`) console argument.

* Windows console prints junk symbols when colors are enabled.

    The default Windows console/terminal cannot print [so called *ansi*] colors, but this is 
    <a href="https://superuser.com/questions/413073/windows-console-with-ansi-colors-handling">fixable</a>
    , especially with modern Windows versions. If for some reason the colors are wrongly enabled by default,
    you can force disable colors by passing `--color-scheme none` console argument.
    
* Bash tools like grep sometimes fail to digest the output when used with pipes (`|`) because of colors.

    Please disable colors by passing `--color-scheme none` console argument.
    The choice for keeping colors in piped output was made to allow convenient usage of `head`, `tail`, file redirection etc.
    In cases like `| grep` it might have issues, in which case you can disable colors.
    
* Output redirected to a file in `> output.txt` manner has no colors when I `cat` it.

    This is considered a rare use case, so colors are disabled by default when outputting to a file.
    But you can force enable colors by passing `--color-scheme common` (for complete list of colors pass `--help`) console argument.
  
* `activate_by_import` or `override_print_tb` don't work in Jupiter or IPython as if not called at all.

    Don't forget to use `ipython=True` or import `activate_in_ipython_by_import` since Jupyer/Ipython handles exceptions differently than regular Python.  
  
* My code doesn't work.  

    Please <a href="https://gitter.im/andy-landy/traceback-with-variables">post your case</a>. You are very welcome!
    
* Other questions or requests to elaborate answers.

    Please <a href="https://gitter.im/andy-landy/traceback-with-variables">post your question or request</a>. You are very welcome! 
