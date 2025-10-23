# How to contribute

Welcome to contribute! The general todo list is this:

* discuss the idea in the chat
* get the informal approve
* go to Testing

## Color Schemes

If you have a nice color scheme, pls proceed to contributing it, some details on how to do it are in FAQ.
You can also ask in the chat.

## The rest of the code

This package was written because other tools' code looked overly complex or hard to read or error-prone to use :) 
Therefore there are some codestyle guidelines applied:
* code transparent for linter
* type annotations everywhere
* no `**kwargs`, `*args`, dicts-instead-of-objects
* no classes other than simple dataclasses with create-like methods
* naming that requires to remember as few things as possible
* no overrides with `if arg is None` logic inside

## Testing

* add new test cases using `assert_smart_equals_ref`
* create new dump files and check coverage by running
    * `PYTHONHASHSEED=1 PYTEST_UPDATE_DUMPS=1 python3 -m pytest -s --cov=./traceback_with_variables --cov-report=json`
    * `python3 check_coverage_reports.py --inp-dir . --max-allowed-num-uncovered-lines 0`
* create a pull request to `next_version` branch
