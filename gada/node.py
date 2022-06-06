"""Package containing everything for manipulating nodes."""
from __future__ import annotations

__all__ = [
    "NodeNotFoundError",
    "Param",
    "Node",
    "NodeCall",
    "NodePath",
    "nodes",
    "dump_module_config",
    "load_module_config",
]
import importlib
from dataclasses import dataclass
from types import ModuleType
from typing import Optional, Any, Tuple, Union
from pathlib import Path
import yaml
from gada import typing
from gada import parser


_GADA_YML_FILENAME = "gada.yml"
_GADA_LANG_MODULE = "gada._lang"


class NodeNotFoundError(Exception):
    def __init__(self, node: str):
        super().__init__(f"node {node} not found")


def _get_cached(cache: dict, mod: ModuleType, key: str, /, defaults: Any = None) -> Any:
    if cache is None or mod not in cache or key not in cache[mod]:
        return defaults

    return cache[mod][key]


def _set_cached(cache: dict, mod: ModuleType, key: str, val: Any) -> None:
    if cache is None:
        return

    cache.setdefault(mod, {})[key] = val


def _locate_module(
    module: Union[ModuleType, str, list[str]], /, *, cache: Optional[dict] = None
) -> Tuple[ModuleType, Path]:
    """Locate a module installed in ``PYTHONPATH``.

    This will raise ``ModuleNotFoundError`` if the module is not installed.

    :param module: module or name
    :param cache: cache for storing results
    :return: a tuple (module, absolute path)
    """
    if not isinstance(module, ModuleType):
        if not isinstance(module, str):
            module = ".".join(module)

        module = importlib.import_module(module)

    path = _get_cached(cache, module, "location")
    if path is None:
        path = Path(module.__file__).parent.absolute()
        _set_cached(cache, module, "location", path)

    return module, path


def dump_module_config(
    module: Union[ModuleType, str, list[str]],
    /,
    config: dict,
    *,
    cache: Optional[dict] = None,
) -> dict:
    r"""Dump ``gada.yml`` to a module installed in ``PYTHONPATH``.

    .. code-block:: python

        >>> import gada
        >>>
        >>> gada.dump_module_config('test.testnodes', {'a': 'b'})
        >>> gada.dump_module_config(['test', 'testnodes'], {'a': 'b'})
        >>>
        >>> from test import testnodes
        >>> gada.dump_module_config(testnodes, {'a': 'b'})
        >>>

    This will raise ``ModuleNotFoundError`` if the module is not installed.

    :param module: module or path
    :param config: configuration to dump
    """
    mod, path = _locate_module(module)

    _set_cached(cache, mod, "config", None)
    with open(path / _GADA_YML_FILENAME, "w+") as f:
        f.write(yaml.safe_dump(config))


def load_module_config(
    module: Union[ModuleType, str, list[str]], /, *, cache: Optional[dict] = None
) -> dict:
    r"""Load ``gada.yml`` from a module installed in ``PYTHONPATH``.

    .. code-block:: python

        >>> import gada
        >>>
        >>> gada.dump_module_config('test.testnodes', {'a': 'b'})
        >>> gada.load_module_config('test.testnodes')
        {'a': 'b'}
        >>> gada.load_module_config(['test', 'testnodes'])
        {'a': 'b'}
        >>>
        >>> from test import testnodes
        >>> gada.load_module_config(testnodes)
        {'a': 'b'}
        >>>

    This will raise ``ModuleNotFoundError`` if the module is not installed.

    :param module: module or path
    :param cache: cache for storing results
    :return: configuration
    """
    mod, path = _locate_module(module)

    conf = _get_cached(cache, mod, "config")
    if conf is None:
        try:
            with open(path / _GADA_YML_FILENAME, "r") as f:
                conf = yaml.safe_load(f.read())
        except FileNotFoundError:
            conf = {}

        _set_cached(cache, mod, "config", conf)

    return conf


def nodes(
    module: Union[ModuleType, str, list[str]], /, *, cache: Optional[dict] = None
) -> list[dict]:
    r"""Get nodes defined in a module.

    .. code-block:: python

        >>> import gada
        >>>
        >>> gada.dump_module_config(
        ...     'test.testnodes',
        ...     {
        ...         'nodes': [
        ...             {'name': 'max'},
        ...             {'name': 'min'}
        ...         ]
        ...     }
        ... )
        >>>
        >>> gada.nodes('test.testnodes')
        [{'name': 'max'}, {'name': 'min'}]
        >>> gada.nodes(['test', 'testnodes'])
        [{'name': 'max'}, {'name': 'min'}]
        >>>
        >>> from test import testnodes
        >>> gada.nodes(testnodes)
        [{'name': 'max'}, {'name': 'min'}]
        >>>

    This will raise ``ModuleNotFoundError`` if the module is not installed.

    :param module: module or path
    :param cache: cache for storing results
    :return: a list of nodes
    """
    return load_module_config(module, cache=cache).get("nodes", [])


@dataclass(frozen=True)
class Param(object):
    """Represent an input or output of a node.

    :param name: name of parameter
    :param type: it's type
    :param help: description of the parameter
    """

    name: str
    value: Any
    type: typing.Type
    help: str

    def __init__(
        self,
        name: str,
        *,
        value: Optional[Any] = None,
        type: Optional[typing.Type] = None,
        help: Optional[str] = None,
    ) -> None:
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "help", help)

    @staticmethod
    def from_config(config: dict, /) -> Param:
        r"""Load a **Param** from a JSON configuration.

        .. code-block:: python

            >>> from gada.node import Param
            >>>
            >>> Param.from_config({"name": "a", "type": "int"})
            Param(name='a', ...)
            >>>

        :param config: configuration
        :return: loaded **Param**
        """
        name = config.get("name", None)
        if not name:
            raise Exception("missing name attribute for node parameter")

        type = config.get("type", None)
        if type:
            type = parser.type(type)

        return Param(
            name=name,
            value=config.get("value", None),
            type=type,
            help=config.get("help", None),
        )


@dataclass(frozen=True)
class Node(object):
    """Represent a node definition.

    :param name: name of the node
    :param module: parent module
    :param file: absolute path to the source code
    :param lineno: line number in the source code
    :param runner: name of runner
    :param is_pure: if the node is pure
    :param inputs: inputs of the node
    :param outputs: outputs of the node
    :param extra: extra parameters
    """
    name: str
    module: ModuleType
    file: Path
    lineno: int
    runner: str
    is_pure: bool
    inputs: list[Param]
    outputs: list[Param]
    extras: dict

    def __init__(
        self,
        name: str,
        *,
        module: Optional[ModuleType] = None,
        file: Optional[Path] = None,
        lineno: Optional[int] = None,
        runner: Optional[str] = None,
        is_pure: Optional[bool] = None,
        inputs: Optional[list[Param]] = None,
        outputs: Optional[list[Param]] = None,
        extras: Optional[dict] = None
    ) -> None:
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "module", module)
        object.__setattr__(self, "file", file)
        object.__setattr__(self, "lineno", lineno if lineno is not None else 0)
        object.__setattr__(self, "runner", runner)
        object.__setattr__(self, "is_pure", is_pure)
        object.__setattr__(self, "inputs", inputs if inputs is not None else [])
        object.__setattr__(self, "outputs", outputs if outputs is not None else [])
        object.__setattr__(self, "extras", extras if extras is not None else {})

    @staticmethod
    def from_config(config: dict, /, *, module: Optional[ModuleType] = None) -> Node:
        r"""Load a **Node** from a JSON configuration.

        .. code-block:: python

            >>> from gada.node import Node
            >>>
            >>> Node.from_config({
            ...   "name": "min",
            ...   "inputs": [
            ...     {"name": "a", "type": "int"},
            ...     {"name": "b", "type": "int"}
            ...   ],
            ...   "outputs": [
            ...     {"name": "out", "type": "int"}
            ...   ]
            ... })
            ...
            Node(name='min', ...)
            >>>

        :param config: configuration
        :param module: parent module
        :return: loaded **Node**
        """
        name = config.pop("name", None)
        if not name:
            raise Exception("missing name attribute for node")

        return Node(
            name=name,
            module=module,
            file=config.pop("file", None),
            lineno=config.pop("lineno", None),
            runner=config.pop("runner", None),
            is_pure=config.pop("pure", False),
            inputs=[Param.from_config(_) for _ in config.pop("inputs", [])],
            outputs=[Param.from_config(_) for _ in config.pop("outputs", [])],
            extras=config
        )


@dataclass(frozen=True)
class NodePath(object):
    r"""Path to a node installed in the **PYTHONPATH**.

    .. code-block:: python

        >>> n = NodePath('module/node')
        >>> repr(n)
        "NodePath('module/node')"
        >>> str(n)
        'module/node'
        >>>

    :param path: node path
    """
    __slots__ = ("_path", "_module", "_name")

    def __init__(self, path: str, /) -> None:
        path = path if path is not None else ""
        parts = path.split("/")
        object.__setattr__(self, "_path", path)
        object.__setattr__(
            self, "_module", parts[:-1] if len(parts) > 1 else _GADA_LANG_MODULE
        )
        object.__setattr__(self, "_name", parts[-1] if len(parts) > 0 else None)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self._path}')"

    def __str__(self) -> str:
        return self._path

    @property
    def module(self) -> list[str]:
        """Name of the parent module"""
        return self._module

    @property
    def name(self) -> str:
        """Name of the node"""
        return self._name

    def absolute(self, *, cache: Optional[dict] = None) -> Path:
        """Get the absolute path to parent module.

        This will raise **ModuleNotFoundError** if module is not in the **PYTHONPATH**.

        :param cache: cache for storing results
        """
        _, path = _locate_module(self._module, cache=cache)
        return path

    def load(self, *, cache: Optional[dict] = None) -> Node:
        r"""Load the node pointed by this path.

        .. code-block:: python

            >>> NodePath('max').load()
            Node(name='max', ...)
            >>>

        This will raise **ModuleNotFoundError** if module is not in the **PYTHONPATH**.

        :param cache: cache for storing results
        :return: the node if it exists
        """
        try:
            mod, _ = _locate_module(self._module)

            conf = load_module_config(mod, cache=cache)
            for _ in conf.get("nodes", []):
                if _.get("name", None) == self._name:
                    return Node.from_config(_, module=mod)
        except Exception:
            pass

        raise NodeNotFoundError(self)

    def exists(self, *, cache: Optional[dict] = None) -> bool:
        r"""Whether this node exists.

        .. code-block:: python

            >>> import gada
            >>>
            >>> gada.NodePath('max').exists()
            True
            >>> gada.NodePath('unknown').exists()
            False
            >>>

        :param cache: cache for storing results
        :return: if the node exists
        """
        try:
            self.load(cache=cache)
            return True
        except Exception:
            return False


@dataclass(frozen=True)
class NodeCall(object):
    """Represent the call to a node in a program.

    :param name: name of the node
    :param id: unique id of the call
    :param file: absolute path to the source code
    :param lineno: line number in the source code
    :param inputs: inputs for the call
    """

    name: str
    id: str
    file: Path
    lineno: int
    inputs: list[Param]

    def __init__(
        self,
        name: str,
        *,
        id: Optional[str] = None,
        file: Optional[Path] = None,
        lineno: Optional[int] = None,
        inputs: Optional[list[Param]] = None,
    ) -> None:
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "id", id)
        object.__setattr__(self, "file", file)
        object.__setattr__(self, "lineno", lineno if lineno is not None else 0)
        object.__setattr__(self, "inputs", inputs if inputs is not None else [])

    @staticmethod
    def from_config(config: dict, /) -> NodeCall:
        r"""Load a **Node** call from a JSON configuration.

        .. code-block:: python

            >>> from gada.node import NodeCall
            >>>
            >>> NodeCall.from_config({
            ...   "name": "min",
            ...   "inputs": {
            ...     "a": 1,
            ...     "b": 2
            ...   }
            ... })
            ...
            NodeCall(name='min', ...)
            >>>

        :param config: configuration
        :return: loaded **NodeCall**
        """
        name = config.get("name", None)
        if not name:
            raise Exception("missing name attribute for node call")

        return NodeCall(
            name=name,
            id=config.get("id", None),
            file=config.get("file", None),
            lineno=config.get("lineno", None),
            inputs={k: v for k, v in config.get("inputs", {}).items()},
        )
