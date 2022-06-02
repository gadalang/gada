__all__ = [
    "NodeNotFoundError",
    "Node",
    "NodeCall",
    "NodePath",
    "NodeInstance",
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


@dataclass
class Node(object):
    __slots__ = "_config"

    def __init__(
        self,
        config: Optional[dict] = None,
        /,
        *,
        name: Optional[str] = None,
        is_pure: Optional[bool] = None,
        runner: Optional[str] = None,
        inputs: Optional[list[dict]] = None,
        outputs: Optional[list[dict]] = None,
    ) -> None:
        self._config = {
            "name": name if name is not None else "",
            "pure": is_pure if is_pure is not None else False,
            "runner": runner if runner is not None else "",
            "inputs": inputs if inputs is not None else [],
            "outputs": outputs if outputs is not None else [],
        } | (config if config is not None else {})

    @property
    def name(self) -> str:
        return self._config.get("name", "")

    @property
    def is_pure(self) -> bool:
        return self._config.get("pure", False)

    @property
    def runner(self) -> str:
        return self._config.get("runner", "")

    def __repr__(self) -> str:
        return f"Node({self._config})"


@dataclass
class NodePath(object):
    __slots__ = ("_path", "_module", "_name")

    def __init__(self, path: str, /) -> None:
        r"""Get a path to a node.

        .. code-block:: python

            >>> import gada
            >>> gada.NodePath('module/node')
            NodePath('module/node')
            >>>

        :param path: node path
        """
        path = path if path is not None else ""
        parts = path.split("/")
        self._path = path
        self._module = parts[:-1] if len(parts) > 1 else _GADA_LANG_MODULE
        self._name = parts[-1] if len(parts) > 0 else None

    def __repr__(self) -> str:
        return f"NodePath('{self._path}')"

    def __str__(self) -> str:
        return self._path

    @property
    def module(self) -> list[str]:
        """Get module path"""
        return self._module

    @property
    def name(self) -> str:
        """Get node name"""
        return self._name

    def absolute(self, *, cache: Optional[dict] = None) -> Path:
        """Get the absolute path to module containing this node.

        This will raise ``ModuleNotFoundError`` if the node is not installed.

        :param cache: cache for storing results
        """
        _, path = _locate_module(self._module, cache=cache)
        return path

    def load(self, *, cache: Optional[dict] = None) -> Node:
        r"""Load the node pointed by this path.

        .. code-block:: python

            >>> import gada
            >>> gada.dump_module_config(
            ...     'test.testnodes',
            ...     {'nodes': [{'name': 'max'}]}
            ... )
            >>>
            >>> gada.NodePath('test/testnodes/max').load()
            Node({...})
            >>>

        This will raise ``NodeNotFoundError`` if the node is not installed.

        :param cache: cache for storing results
        :return: the node if it exists
        """
        try:
            conf = load_module_config(self._module, cache=cache)
            for _ in conf.get("nodes", []):
                if _.get("name", None) == self._name:
                    return Node(_)
        except Exception:
            pass

        raise NodeNotFoundError(self)

    def exists(self, *, cache: Optional[dict] = None) -> bool:
        r"""Whether this node exists.

        .. code-block:: python

            >>> import gada
            >>> gada.dump_module_config(
            ...     'test.testnodes',
            ...     {'nodes': [{'name': 'max'}]}
            ... )
            >>>
            >>> gada.NodePath('test/testnodes/max').exists()
            True
            >>> gada.NodePath('test/testnodes/min').exists()
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


@dataclass
class NodeCall(object):
    __slots__ = "_config"

    def __init__(
        self,
        config: Optional[dict] = None,
        /,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,
        line: Optional[int] = None,
        inputs: Optional[dict] = None,
        outputs: Optional[dict] = None,
    ) -> None:
        self._config = {
            "name": name if name is not None else "",
            "id": id if id is not None else "",
            "line": line if line is not None else 0,
            "inputs": dict(inputs) if inputs is not None else {},
            "outputs": dict(outputs) if outputs is not None else {},
        } | (config if config is not None else {})

    @property
    def name(self) -> str:
        return self._config.get("name", "")

    @property
    def id(self) -> str:
        return self._config.get("id", "")

    @property
    def line(self) -> int:
        return self._config.get("line", 0)

    @property
    def inputs(self) -> dict:
        return self._config.get("inputs", {})

    @property
    def outputs(self) -> dict:
        return self._config.get("outputs", {})

    def __repr__(self) -> str:
        return f"NodeCall({self._config})"


@dataclass
class NodeInstance(object):
    __slot__ = ("_node", "_step", "_outputs")

    def __init__(
        self, node: Node, step: NodeCall, /, outputs: Optional[dict] = None
    ) -> None:
        self._node: Node = node
        self._step: NodeCall = step
        self._outputs: dict = outputs if outputs is not None else {}

    @property
    def node(self) -> Node:
        return self._node

    @property
    def step(self) -> NodeCall:
        return self._step

    @property
    def outputs(self) -> dict:
        return self._outputs

    def var(self, name: str, /) -> Any:
        return self._outputs.get(name, None)

    def __repr__(self) -> str:
        return f"NodeInstance({self._node}, {self._step}, {self._output})"
