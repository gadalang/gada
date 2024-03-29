"""Cache for runtime data."""
from __future__ import annotations

__all__ = [
    "clear",
    "load_module",
    "get_module_path",
    "load_module_config",
    "dump_module_config",
    "get_cached_node",
    "set_cached_node",
]
from types import ModuleType
from typing import TYPE_CHECKING
import importlib
from pkgutil import ModuleInfo
from pathlib import Path
import yaml

if TYPE_CHECKING:
    from typing import Any, Union, Iterable

    ModuleLike = Union[ModuleInfo, ModuleType, str, Iterable[str]]

_GADA_YML_FILENAME = "gada.yml"
_LOAD_MODULE_CACHE = {}
_MODULE_PATH_CACHE = {}
_MODULE_CONFIG_CACHE = {}
_MODULE_NODE_CACHE = {}


def clear() -> None:
    """Clear the cache"""
    global _LOAD_MODULE_CACHE, _MODULE_PATH_CACHE, _MODULE_CONFIG_CACHE, _MODULE_NODE_CACHE
    _LOAD_MODULE_CACHE = {}
    _MODULE_PATH_CACHE = {}
    _MODULE_CONFIG_CACHE = {}
    _MODULE_NODE_CACHE = {}


def load_module(module: ModuleLike, /) -> ModuleType:
    """Load a module by path and cache the result.

    This will raise **ModuleNotFoundError** if the module is not installed.

    :param module: name or path to module
    :return: loaded module
    """
    if isinstance(module, ModuleType):
        return module

    if isinstance(module, ModuleInfo):
        module = module.name
    elif isinstance(module, list):
        module = ".".join(module)

    mod = _LOAD_MODULE_CACHE.get(module, None)
    if mod is None:
        mod = importlib.import_module(module)
        _LOAD_MODULE_CACHE[module] = mod

    return mod


def get_module_path(module: ModuleLike, /) -> Path:
    """Locate a module installed in **PYTHONPATH**.

    This will raise **ModuleNotFoundError** if the module is not installed.

    :param module: name or path to module
    :return: a tuple (module, absolute path)
    """
    mod = load_module(module)

    path = _MODULE_PATH_CACHE.get(mod, None)
    if path is None:
        if isinstance(mod, ModuleInfo):
            path = Path(mod.module_finder.path) / mod.name
        else:
            path = Path(mod.__file__).parent
        path = path.absolute()
        _MODULE_PATH_CACHE[mod] = path

    return path


def load_module_config(module: ModuleLike) -> dict:
    r"""Load ``gada.yml`` from a module installed in **PYTHONPATH**.

    This will raise **ModuleNotFoundError** if the module is not installed.

    :param module: name or path to module
    :return: configuration
    """
    mod = load_module(module)

    conf = _MODULE_CONFIG_CACHE.get(mod, None)
    if conf is None:
        path = get_module_path(mod)
        try:
            with open(path / _GADA_YML_FILENAME, "r") as f:
                conf = yaml.safe_load(f.read())
        except FileNotFoundError:
            conf = {}

        _MODULE_CONFIG_CACHE[mod] = conf

    return conf


def dump_module_config(module: ModuleLike, /, config: dict) -> None:
    r"""Dump ``gada.yml`` to a module installed in **PYTHONPATH**.

    This will raise **ModuleNotFoundError** if the module is not installed.

    :param module: module or path
    :param config: configuration to dump
    """
    mod = load_module(module)
    path = get_module_path(mod)

    _MODULE_CONFIG_CACHE[mod] = None
    with open(path / _GADA_YML_FILENAME, "w+") as f:
        f.write(yaml.safe_dump(config))


def get_cached_node(module: ModuleType, name: str, /) -> Any:
    cache = _MODULE_NODE_CACHE.get(module, None)
    if not cache:
        return None

    return cache.get(name, None)


def set_cached_node(module: ModuleType, name: str, node: Any, /) -> None:
    _MODULE_NODE_CACHE.setdefault(module, {})[name] = node
