from traceback_with_variables import Format, ColorSchemes, is_ipython_global, fmt, hide, skip


# approach 1 for simples usage

fmt.max_value_str_len = 10000

# show all vars, no hides, no skips:

fmt.custom_var_printers = []


# approach 2 for explicit format passing

fmt2 = Format(
    before=3,
    after=1,
    max_value_str_len=10000,
    objects_details=0,
    ellipsis_rel_pos=0.7
    max_exc_str_len=1000,
    ellipsis_='...',
    color_scheme=ColorSchemes.synthwave,
    skip_files_except=['my_project', 'site-packages'],
    brief_files_except='my_project',
    custom_var_printers=[  # first matching is used
        ('password', hide),  # by name, print const str
        (list, lambda v: f'list{v}'),  # by type, print fancy str
        (lambda name, type_, filename, is_global: is_global, skip),  # custom filter, skip printing
        (is_ipython_global, lambda v: None),  # same, handy for Jupyter
        (['secret', dict, (lambda name, *_: 'asd' in name)], lambda v: '???'),  # by different things, print const str
    ]
)
print_exc(fmt=fmt2)


# approach 3 for explicit format passing, less code

fmt3 = defaults.replace(max_value_str_len=10000)
print_exc(fmt=fmt3)
