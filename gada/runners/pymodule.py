"""Run nodes from Python modules.
"""
from __future__ import annotations

__all__ = ["run"]
from gada.node import Node


def _load_module(name: str):
    try:
        import importlib

        return importlib.import_module(name)
    except Exception as e:
        raise Exception(f"failed to import module {name}") from e


def run(node: Node, *, inputs: dict) -> dict:
    r"""Run a node contained in a Python module.
    
    :param node: node definition
    :param inputs: node inputs
    :return: node outputs
    """
    argv = argv if argv is not None else []

    # Check the entrypoint is configured
    entrypoint = node.extras.get("entrypoint", None)
    if not entrypoint:
        raise Exception(f"missing entrypoint for node {node.name}")

    # Load module if explicitely configured
    mod = _load_module(node.extras["module"]) if "module" in node.extras else node.module

    # Check the entrypoint exists
    fun = getattr(mod, entrypoint, None)
    if not fun:
        raise Exception(f"module {mod.__name__} has no entrypoint {entrypoint}")

    # Call entrypoint
    return fun(inputs=inputs)
