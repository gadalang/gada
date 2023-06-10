import pytest
import gada
from gada import _cache, _lang
import conftest


TEST_MODULE = "gada._lang"


@conftest.clean_test
def test_load_gada_module():
    """Test loading the gada module"""
    assert _cache.load_module("gada").__name__ == gada.__name__


@conftest.clean_test
def test_load_gadalang_module():
    """Test locating the gada._lang submodule"""
    assert _cache.load_module("gada._lang").__name__ == _lang.__name__


@conftest.clean_test
def test_load_module_fail():
    """Test an error is raised when trying to load an invalid module"""
    with pytest.raises(ModuleNotFoundError):
        _cache.load_module("invalidmodule")


@conftest.clean_test
def test_dump_module_config():
    """Test dumping ``testnodes/gada.yml`` with ``dump_module_config``"""
    _cache.dump_module_config("test.testnodes", conftest.CONFIG_NO_RUNNER)
    assert (
        conftest.load_module_config() == conftest.CONFIG_NO_RUNNER
    ), "wrong configuration"


@conftest.clean_test
def test_dump_module_config_fail():
    """Test dumping ``gada.yml`` to an invalid module`"""
    with pytest.raises(ModuleNotFoundError):
        _cache.dump_module_config("invalidmodule", conftest.CONFIG_NO_RUNNER)


@conftest.clean_test
@conftest.with_module_config(config=conftest.CONFIG_NO_RUNNER)
def test_load_module_config():
    """Test loading ``testnodes/gada.yml`` with ``load_module_config``"""
    assert (
        _cache.load_module_config("test.testnodes") == conftest.CONFIG_NO_RUNNER
    ), "wrong configuration"


def test_load_module_config_fail():
    """Test loading ``gada.yml`` from an invalid module"""
    with pytest.raises(ModuleNotFoundError):
        _cache.load_module_config("invalidmodule")


@conftest.clean_test
@conftest.with_module_config(config=conftest.CONFIG_NO_RUNNER)
def test_load_module_config_cache():
    """Test caching results of ``load_module_config``"""
    # First time config is not cached
    c1 = _cache.load_module_config("test.testnodes")
    assert c1 == conftest.CONFIG_NO_RUNNER, "wrong configuration"
    # Second time should return the cached object
    c2 = _cache.load_module_config("test.testnodes")
    assert c2 == conftest.CONFIG_NO_RUNNER, "wrong configuration"
    assert id(c1) == id(c2), "dit not return from cache"

    # Will clear the cache
    _cache.dump_module_config("test.testnodes", conftest.CONFIG_NO_RUNNER)
    c3 = _cache.load_module_config("test.testnodes")
    assert c3 == conftest.CONFIG_NO_RUNNER, "wrong configuration"
    assert id(c1) != id(c3), "dit not return from cache"
