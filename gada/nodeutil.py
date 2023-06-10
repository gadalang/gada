"""Package containing everything for manipulating nodes."""
from __future__ import annotations

__all__ = [
    "NodeNotFoundError",
    "Param",
    "Node",
    "NodeCall",
    "NodePath",
    "nodes",
    "iter_packages",
    "iter_nodes",
    "create_parser",
]
from typing import TYPE_CHECKING
import pkgutil
import argparse
from dataclasses import dataclass
from types import ModuleType
from pathlib import Path
from gada import typing, _cache, gadayml
from gada._log import logger

if TYPE_CHECKING:
    from typing import Iterable
    from pkgutil import ModuleInfo

    from gada.gadayml import GadaConfig, NodeConfig


_GADA_LANG_MODULE = "gada._lang"


class PackageInfo:
    def __init__(self, path: Path, name: str, gada_yml_path: Path) -> None:
        self.path = path
        self.name = name
        self.gada_yml_path = gada_yml_path


class NodeInfo:
    def __init__(self, package_info: PackageInfo, config: NodeConfig) -> None:
        self.package_info = package_info
        self.config = config


class NodeNotFoundError(Exception):
    def __init__(self, node: str):
        super().__init__(f"node {node} not found")


def iter_packages(path: list[str] | None = None) -> Iterable[PackageInfo]:
    """Yield Python packages having a top-level gada.yml file.

    .. code-block:: python

        >>> from gada import nodeutil
        >>>
        >>> for package in nodeutil.iter_packages():
        ...     print(package.name)
        >>>
        gada
        >>>

    :param path: should be either None or a list of paths to look for modules in
    """
    for mod in pkgutil.iter_modules(path):
        if not hasattr(mod.module_finder, "path"):
            continue

        gada_yml_path = Path(mod.module_finder.path) / mod.name / "gada.yml"
        if gada_yml_path.exists():
            yield PackageInfo(
                path=mod.module_finder.path, name=mod.name, gada_yml_path=gada_yml_path
            )


def iter_nodes(path: list[str] | None = None) -> Iterable[NodeInfo]:
    r"""Yield installed Gada nodes.

    .. code-block:: python

        >>> from gada import nodeutil
        >>>
        >>> for node in nodeutil.iter_nodes():
        ...     print(node.name)
        >>>
        rebuild
        >>>

    :param path: should be either None or a list of paths to look for modules in
    """
    for package in iter_packages(path):
        config = gadayml.load(package.name)
        for node in config["nodes"]:
            yield NodeInfo(package_info=package, config=node)


def find_node(name: str) -> NodeInfo | None:
    """Find a node by name.

    :param name: name of the node
    """
    for node in iter_nodes():
        if node.config["name"] == name:
            return node

    return node


def create_parser(node: NodeInfo | str) -> argparse.ArgumentParser:
    if isinstance(node, str):
        if (info := find_node(node)) is None:
            raise Exception("node not found")

        node = info

    parser = argparse.ArgumentParser(node.config["name"])
    if inputs := node.config["input"]:
        for input in inputs:
            kwargs = {}
            if "action" in input:
                kwargs["action"] = input["action"]

            if "nargs" in input:
                kwargs["nargs"] = input["nargs"]

            parser.add_argument(input["name"], **kwargs)

    return parser


def load(node: NodeInfo | str) -> None:
    if isinstance(node, str):
        if (info := find_node(node)) is None:
            raise Exception("node not found")

        node = info

    mod = _cache.load_module(node.package_info.name)
    fun = getattr(mod, node.config["name"], None)
    print(fun)


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
