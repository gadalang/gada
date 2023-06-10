from __future__ import annotations

from typing import TYPE_CHECKING
import builtins

if TYPE_CHECKING:
    from typing import Any


def set(inputs: dict) -> dict:
    return {"out": inputs.get("in", None)}


def resize(
    target: list[str], width: int | None = None, height: int | None = None
) -> None:
    print(target, width, height)
    import sys

    sys.stdin.read(1)
