"""
When you deal with secrets like passwords or tokens any debug report system
puts you at risk of exposing those secrets. 

Why? Some secrets are stored securely in databases and are kept decrypted only
for short time in memory while being used in code. So any traceback printout 
will save them explicitly for you to read later. 

Its not a huge problem if the secret is stored unencrypted, i.e. its your
(not users') secret and the machine is secure. User passwords are a problem.

How to prevent secret vars from being printed? You might
    * correctly guess how the secret variables in your code are called
    * hide the 3rd party well-established library code totally

It will look like this: some of variables in your code will have
"...hidden..." values, and all library files (where secret variables might go
with unrelated names like "s", "part", "msg" etc.) will be skipped totally.

Default settings include all frequent patterns for your variables:
    PATTERN_TO_HIDE = '.*(?i:pass|secret|token|key|api_key|cred|pwd).*'
Which will hide a bit too much, names like "keyword" or "compassion". Address
examples below to fit the hiding.

To hide libraries address examples below, note that you can only allow code,
not deny it, so all 3rd party libraries will be hidden if you use this
setting.
"""

# simple tools usage, for more manual approach address format_customized.py

from traceback_with_variables import fmt, hide


# hide all libraries except couple

fmt.brief_files_except = ['.*my_project.*', '.*some_library_1.*', '.*some_library_2.*']


# show all variables

fmt.custom_var_printers = []


# hide variables differently

fmt.custom_var_printers = [
    ('.*(precious|ring).*', hide),  # by name
    (MySecret, hide),  # by class
]
