import pytest
from gada import _model
import conftest


def test_locate_module():
    '''Test locating the gada module'''
    _, p = _model._locate_module('gada')
    assert p.name == 'gada', 'failed to locate gada module'


def test_locate_submodule():
    '''Test locating the gada.runners submodule'''
    _, p = _model._locate_module('gada.runners')
    assert p.name == 'runners', 'failed to locate gada.runners module'


def test_locate_module_fail():
    '''Test an error is raised when trying to locate an invalid module'''
    with pytest.raises(ModuleNotFoundError):
        _model._locate_module('invalidmodule')


def test_locate_module_cache():
    '''Test caching results of ``locate_module``'''
    cache = {}
    # First time path is not cached
    _, p1 = _model._locate_module('gada', cache=cache)
    assert p1.name == 'gada', 'failed to locate gada module'
    # Second time should return the cached object
    _, p2 = _model._locate_module('gada', cache=cache)
    assert id(p1) == id(p2), 'dit not return from cache'


@conftest.clean_test
def test_dump_module_config():
    '''Test dumping ``testnodes/gada.yml`` with ``dump_module_config``'''
    _model.dump_module_config('test.testnodes', conftest.CONFIG_NO_RUNNER)
    assert conftest.load_module_config() == conftest.CONFIG_NO_RUNNER, 'wrong configuration'


def test_dump_module_config_fail():
    '''Test dumping ``gada.yml`` to an invalid module`'''
    with pytest.raises(ModuleNotFoundError):
        _model.dump_module_config('invalidmodule', conftest.CONFIG_NO_RUNNER)


@conftest.clean_test
@conftest.with_module_config(config=conftest.CONFIG_NO_RUNNER)
def test_load_module_config():
    '''Test loading ``testnodes/gada.yml`` with ``load_module_config``'''
    assert _model.load_module_config('test.testnodes') == conftest.CONFIG_NO_RUNNER, 'wrong configuration'


def test_load_module_config_fail():
    '''Test loading ``gada.yml`` from an invalid module'''
    with pytest.raises(ModuleNotFoundError):
        _model.load_module_config('invalidmodule')


@conftest.clean_test
@conftest.with_module_config(config=conftest.CONFIG_NO_RUNNER)
def test_load_module_config_cache():
    '''Test caching results of ``load_module_config``'''
    cache = {}
    # First time config is not cached
    c1 = _model.load_module_config('test.testnodes', cache=cache)
    assert c1 == conftest.CONFIG_NO_RUNNER, 'wrong configuration'
    # Second time should return the cached object
    c2 = _model.load_module_config('test.testnodes', cache=cache)
    assert c2 == conftest.CONFIG_NO_RUNNER, 'wrong configuration'
    assert id(c1) == id(c2), 'dit not return from cache'

    # Will clear the cache
    _model.dump_module_config('test.testnodes', conftest.CONFIG_NO_RUNNER, cache=cache)
    c3 = _model.load_module_config('test.testnodes', cache=cache)
    assert c3 == conftest.CONFIG_NO_RUNNER, 'wrong configuration'
    assert id(c1) != id(c3), 'dit not return from cache'


@conftest.clean_test
@conftest.with_module_config(config=conftest.CONFIG_NO_RUNNER)
def test_nodes():
    '''Test getting nodes from ``test.testnodes``'''
    assert _model.nodes('test.testnodes') == conftest.CONFIG_NO_RUNNER['nodes'], 'invalid nodes'
