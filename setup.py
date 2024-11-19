import setuptools

from traceback_with_variables import __version__

with open('README.md', 'r', encoding='utf-8') as in_:
    long_description = in_.read()

setuptools.setup(
    name='traceback-with-variables',
    version=__version__,
    author='Andrey Lyashko',
    author_email='andydashlandy@gmail.com',
    description='Adds variables to python traceback. Simple, lightweight, cont'
    'rollable. Debug reasons of exceptions by logging or pretty printing color'
    'ful variable contexts for each frame in a stacktrace, showing every value'
    '. Dump locals environments after errors to console, files, and loggers. W'
    'orks with Jupyter and IPython.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/andy-landy/traceback_with_variables',
    packages=['traceback_with_variables'],
    keywords=['python', 'traceback', 'locals', 'logging', 'debugging', 'print',
              'variables', 'python3', 'stacktrace', 'arguments', 'errors',
              'error-handling', 'dump', 'exception-handling', 'exceptions',
              'pretty', 'pretty-print', 'frame', 'simple',
              'colors', 'jupyter', 'jupyter-notebook', 'ipython', 'customize'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Libraries',
    ],
    entry_points={'console_scripts': [
        'traceback-with-variables = traceback_with_variables.main:main',
    ]},
    tests_require=[
        'flake8',
        'ipython',
        'pytest-cov',
        'notebook==6.2.0',
    ],
    install_requires=[],
    python_requires='>=3.6',
)
