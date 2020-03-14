```
def main():
    args = parse_args()

    with rich_traceback():
        do_something(...)
```

```
RichTraceback (most recent call last):
  File "./temp.py", line 25, in substitute_in_files
    substitute_in_one_file(os.path.join(dir_, filename), old_fragment, new_fragment)
      dir_=test_dir
      filename=file3
      filenames=['file3', 'file2', 'file1']
      new_fragment=FP
      old_fragment=OOP
      root_path=test_dir
      subdirs=[]
  File "./temp.py", line 16, in substitute_in_one_file
    with open(path, 'r') as in_:
      new_fragment=FP
      old_fragment=OOP
      path=test_dir/file3
builtins.PermissionError: [Errno 13] Permission denied: 'test_dir/file3'
```
