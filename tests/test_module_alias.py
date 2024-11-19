import os

import pytest

import traceback_with_variables as twv
from traceback_with_variables.module_alias import create_alias, rm_alias, module_name_to_path, Path


ROOT_PATH = Path(twv.__file__).parent.parent
TWV = 'traceback_with_variables'
OS = 'os'
ALIAS = 'alias'


def test_module_name_to_path():
    assert module_name_to_path(OS) == Path(os.__file__)
    assert module_name_to_path(TWV) == ROOT_PATH / TWV
    with pytest.raises(ModuleNotFoundError):
        module_name_to_path('nonexistant_module')


def test_create_and_rm_alias():
    # problems before we have the alias

    with pytest.raises(ValueError) as e:
        create_alias('', TWV)
    assert str(e.value) == 'the alias must be non-empty'
    
    with pytest.raises(ValueError) as e:
        create_alias('bad name', TWV)
    assert str(e.value) == 'the alias must have only ascii lowecases, digits and underscores'
    
    with pytest.raises(ModuleNotFoundError):
        create_alias(ALIAS, 'nonexistant_module')
    
    with pytest.raises(ValueError) as e:
        create_alias(OS, TWV)
    assert str(e.value) == 'a module with the alias name already exists'    
    
    with pytest.raises(ModuleNotFoundError):
        rm_alias(ALIAS)
    
    with pytest.raises(ValueError) as e:
        rm_alias(TWV)
    
    assert str(e.value) == 'the module is not an alias'
    
    create_alias(ALIAS, TWV)
    
    # problems once we have the alias
    
    with pytest.raises(ValueError) as e:
        create_alias(ALIAS, TWV)
    assert str(e.value) == 'a module with the alias name already exists'
    
    with pytest.raises(ValueError) as e:
        create_alias(ALIAS, OS)
    assert str(e.value) == 'a module with the alias name already exists'
   
    rm_alias(ALIAS)
    
    # problems after we rm the alias

    with pytest.raises(ModuleNotFoundError):
        rm_alias(ALIAS)

    # rare case of garbage in the lib dir

    os.symlink(str(ROOT_PATH / 'nonexistant'), str(ROOT_PATH / ALIAS))
    with pytest.raises(ValueError) as e:
        create_alias(ALIAS, TWV)
    assert str(e.value) == 'the needed file system location already occupied'
    os.remove(str(ROOT_PATH / ALIAS))
