from __future__ import annotations

__all__ = ["dump", "load"]
from typing import TYPE_CHECKING
from pathlib import Path
import yaml
import jsonschema

from gada import _cache

if TYPE_CHECKING:
    from typing import Iterable, TypedDict, Any

    from gada._cache import ModuleLike

    class InputConfig(TypedDict):
        """Configuration of a node."""

        name: str
        """"Name of input."""
        type: str | None
        """automatically convert an argument to the given type."""
        nargs: str | None
        """Number of times the argument can be used."""
        action: str | None
        """specify how an argument should be handled."""

    class MenuConfig(TypedDict):
        """Configuration of a node."""

        type: str
        """Name of the node."""
        path: list[str]
        """Menu entry."""

    class NodeConfig(TypedDict):
        """Configuration of a node."""

        runner: str | None
        """Individual runner."""
        name: str
        """Name of the node."""
        menu: MenuConfig | None
        """Menu entry."""
        input: list[InputConfig] | None
        """Inputs of the node."""

    class GadaConfig(TypedDict):
        """Configuration from gada.yml."""

        runner: str | None
        """Global runner."""
        nodes: list[NodeConfig]
        """List of nodes."""


def load_schema() -> dict[str, Any]:
    """Load the JSON schema for gada.yml files."""
    with open(Path(__file__).parent / "gada.yml.schema") as f:
        return yaml.safe_load(f)


def dump(config: GadaConfig) -> dict[str, Any]:
    r"""Dump ``gada.yml`` to a module installed in **PYTHONPATH**.

    .. code-block:: python

        >>> from gada import node
        >>>
        >>> node.dump_module_config('test.testnodes', {'a': 'b'})
        >>> node.dump_module_config(['test', 'testnodes'], {'a': 'b'})
        >>>
        >>> from test import testnodes
        >>> node.dump_module_config(testnodes, {'a': 'b'})
        >>>

    This will raise **ModuleNotFoundError** if the module is not installed.

    :param module: module or path
    :param config: configuration to dump
    """
    return yaml.safe_dump(_namespace_to_dict(config))


def load(module: ModuleLike, /) -> GadaConfig:
    r"""Load ``gada.yml`` from a module installed in **PYTHONPATH**.

    This will raise **ModuleNotFoundError** if the module is not installed.

    :param module: module or path
    :return: configuration
    """
    config = _cache.load_module_config(module)
    jsonschema.validate(config, load_schema())

    return config
