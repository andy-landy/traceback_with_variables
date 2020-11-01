import setuptools

with open('README.md', 'r') as in_:
    long_description=in_.read()

setuptools.setup(
    name='traceback-with-variables',
    version='1.0.0',
    author='Andrey Lyashko',
    author_email='andrewlyashko@gmail.com',
    description='print traceback with variables, simple to use',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/andy-landy/rich_traceback',
    packages=setuptools.find_packages(),
    keywords=['python', 'traceback', 'locals', 'logging', 'debugging', 'print',
              'variables', 'python3', 'stacktrace', 'arguments'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.4',
)