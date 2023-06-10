from __future__ import annotations

__all__ = ["run"]
from typing import TYPE_CHECKING
from gada import _lang

if TYPE_CHECKING:
    from gada.nodeutil import NodeInfo


def run(node: NodeInfo, *, inputs: dict) -> dict:
    name = node.config["name"]
    fun = getattr(_lang, name, None)
    if not fun:
        raise Exception(f"missing {name} node implementation")

    return fun(**inputs)
