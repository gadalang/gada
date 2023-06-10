"""Run nodes from Python modules.
"""
from __future__ import annotations

__all__ = ["run"]
from typing import TYPE_CHECKING
from pathlib import Path
import yaml
import jsonschema

if TYPE_CHECKING:
    from typing import Any
    from gada.nodeutil import NodeInfo


def _load_module(name: str):
    try:
        import importlib

        return importlib.import_module(name)
    except Exception as e:
        raise Exception(f"failed to import module {name}") from e


def _load_schema() -> dict[str, Any]:
    """Load the JSON schema for gada.yml files."""
    with open(Path(__file__).parent / "pymodule.schema") as f:
        return yaml.safe_load(f)


def run(node: NodeInfo, *, inputs: dict) -> dict:
    r"""Run a node contained in a Python module.

    :param node: node definition
    :param inputs: node inputs
    :return: node outputs
    """
    jsonschema.validate(node.config, _load_schema())
    entrypoint = node.config.get("entrypoint", "").split(".")

    # Load module if explicitely configured
    mod = _load_module(".".join(entrypoint[:-1]))

    # Check the entrypoint exists
    fun = getattr(mod, entrypoint[-1], None)
    if not fun:
        raise Exception(f"module {mod.__name__} has no entrypoint {entrypoint}")

    # Call entrypoint
    return fun(**inputs)
