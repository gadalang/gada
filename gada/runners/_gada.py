__all__ = ["run"]
from gada import Node
from gada import _lang


def run(*, node: Node, inputs: dict, cache: dict = None) -> dict:
    fun = getattr(_lang, f"_{node.name}", None)
    if not fun:
        raise Exception(f"missing {node.name} node implementation")

    return fun(inputs)
