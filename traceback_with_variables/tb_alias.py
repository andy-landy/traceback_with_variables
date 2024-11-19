from traceback_with_variables.module_alias import create_alias, rm_alias


def create_tb_alias() -> None:
    create_alias(alias='tb', module_name='traceback_with_variables')


def rm_tb_alias() -> None:
    rm_alias(alias='tb')
