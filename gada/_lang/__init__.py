from __future__ import annotations

__all__ = ["set", "print", "max", "min"]
import builtins


def set(inputs: dict) -> dict:
    return {"out": inputs.get("in", None)}


def print(inputs: dict) -> dict:
    if "in" in inputs:
        builtins.print(inputs["in"])

    return {}


def max(inputs: dict) -> dict:
    return {"out": builtins.max(inputs.get("a", None), inputs.get("b", None))}


def min(inputs: dict) -> dict:
    return {"out": builtins.min(inputs.get("a", None), inputs.get("b", None))}
