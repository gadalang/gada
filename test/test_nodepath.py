'''Tests on the ``gada.NodePath`` class'''
import pytest
import gada
import conftest


@conftest.clean_test
def test_nodepath():
    p = gada.NodePath('test/testnodes/hello')
    assert repr(p) == "NodePath('test/testnodes/hello')", 'incorrect repr'
    assert str(p) == 'test/testnodes/hello', 'incorrect str'
    assert p.module == ['test', 'testnodes'], 'incorrect module'
    assert p.name == 'hello', 'incorrect name'


@conftest.clean_test
@conftest.with_module_config(config=conftest.CONFIG_HELLO_NODE)
def test_nodepath_load():
    n = gada.NodePath('test/testnodes/hello').load()
    assert n.name == conftest.CONFIG_HELLO_NODE['nodes'][0]['name'], 'wrong configuration'


@conftest.clean_test
@conftest.with_module_config(config=conftest.CONFIG_HELLO_NODE)
def test_nodepath_load_fail():
    with pytest.raises(gada.NodeNotFoundError):
        gada.NodePath('invalidnode').load()


@conftest.clean_test
@conftest.with_module_config(config=conftest.CONFIG_HELLO_NODE)
def test_nodepath_exists():
    assert gada.NodePath('test/testnodes/hello').exists(), 'hello node not found'


@conftest.clean_test
def test_nodepath_absolute():
    p = gada.NodePath('test/testnodes/hello').absolute()
    assert p == conftest.TESTNODES_PATH, 'wrong absolute path'


@conftest.clean_test
def test_nodepath_absolute():
    p = gada.NodePath('test/testnodes/hello').absolute()
    assert p == conftest.TESTNODES_PATH, 'wrong absolute path'


@conftest.clean_test
def test_nodepath_absolute_fail():
    with pytest.raises(ModuleNotFoundError):
        gada.NodePath('invalidmodule/hello').absolute()