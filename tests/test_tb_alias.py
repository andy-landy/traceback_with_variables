import pytest

from traceback_with_variables.tb_alias import create_tb_alias, rm_tb_alias

from tests.test_utils import run_code, dummies_code, tb_reg


def test_create_and_rm_tb_alias(tmp_path, tb_reg):
    tb_reg(run_code(tmp_path, [], ['import tb.a', dummies_code, 'f()'], [], True), 'run 1 without tb')

    create_tb_alias()
    tb_reg(run_code(tmp_path, [], ['import tb.a', dummies_code, 'f()'], [], True), 'run with tb')

    rm_tb_alias()
    tb_reg(run_code(tmp_path, [], ['import tb.a', dummies_code, 'f()'], [], True), 'run 2 without tb')
