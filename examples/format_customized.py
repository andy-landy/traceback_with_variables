from traceback_with_variables import Format, ColorSchemes, is_ipython_global


fmt = Format(
    before=3,
    after=1,
    max_value_str_len=100,
    max_exc_str_len=1000,
    ellipsis_='...',
    color_scheme=ColorSchemes.synthwave,
    skip_files_except=['my_project', 'site-packages'],
    brief_files_except='my_project',
    custom_var_printers=[  # first matching is used
        ('password', lambda v: '...hidden...'),  # by name, print const str
        (list, lambda v: f'list{v}'),  # by type, print fancy str
        (lambda name, type_, filename, is_global: is_global, lambda v: None),  # custom filter, skip printing
        (is_ipython_global, lambda v: None),  # same, handy for Jupyter
        (['secret', dict, (lambda name, *_: 'asd' in name)], lambda v: '???'),  # by different things, print const str
    ]
)
