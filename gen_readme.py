from pathlib import Path

from jinja2 import Template

from traceback_with_variables import __version__ as version


user_name = 'andy-landy'
repo_name = 'traceback_with_variables'
import_name = 'traceback_with_variables'
package_name = 'traceback-with-variables'
user_repo_name = f'{user_name}/{repo_name}'
repo_url = f'https://github.com/{user_repo_name}'
code_url = f'{repo_url}/tree/master'
lib_code_url = f'{code_url}/{import_name}'
examples_code_url = f'{code_url}/examples'
pypi_url = f'https://pypi.org/project/{package_name}'
content_url = f'https://raw.githubusercontent.com/{user_repo_name}/master'
gitter_url = f'https://gitter.im/{user_name}/{package_name}'


Path('README.md').write_text(Template(Path('README.tmpl').read_text()).render(
    user_name=user_name,
    repo_name=repo_name,
    import_name=import_name,
    package_name=package_name,
    user_repo_name=user_repo_name,
    repo_url=repo_url,
    code_url=code_url,
    lib_code_url=lib_code_url,
    examples_code_url=examples_code_url,
    pypi_url=pypi_url,
    content_url=content_url,
    gitter_url=gitter_url,
    version=version,
))
