"""Potentially evil magic to speed up the interactive commands"""

import importlib
import os
import string
from pathlib import Path


VALID_CHARS = set(string.ascii_lowercase + string.digits + '_')


def module_name_to_path(name: str) -> Path:
    spec = importlib.util.find_spec(name)
    if spec is None:
        raise ModuleNotFoundError(name)
    path = Path(spec.origin)
    return path.parent if path.name == '__init__.py' else path


def module_exists(name: str) -> bool:
    try:
        module_name_to_path(name)
    except ModuleNotFoundError:
        return False
    return True


def create_alias(alias: str, module_name: str) -> None:
    if not alias:
        raise ValueError('the alias must be non-empty')
    if any(c not in VALID_CHARS for c in alias):
        raise ValueError('the alias must have only ascii lowecases, digits and underscores')
    if module_exists(alias):
        raise ValueError('a module with the alias name already exists')
    module_path = module_name_to_path(module_name)

    try:
        os.symlink(str(module_path), str(module_path.parent / alias))
    except FileExistsError:
        raise ValueError('the needed file system location already occupied')


def rm_alias(alias: str) -> None:
    module_path = module_name_to_path(alias)
    if not module_path.is_symlink():
        raise ValueError('the module is not an alias')
    os.remove(str(module_path))
