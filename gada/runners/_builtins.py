"""Run a node wrapping a function from the **builtins** module."""
from __future__ import annotations

__all__ = ["run"]
from gada.node import Node


import builtins


def run(node: Node, *, inputs: dict) -> dict:
    fun = getattr(builtins, node.name, None)
    if not fun:
        raise Exception(f"no builtins.{node.name}")

    return {"out": fun(**inputs)}
