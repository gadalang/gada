"""Package containing the builin types usable in gada"""
__all__ = [
    "Type",
    "IntType",
    "FloatType",
    "StringType",
    "BoolType",
    "ListType",
    "TupleType",
    "UnionType",
    "typeof",
]
from dataclasses import dataclass
from typing import Any
from abc import ABC, abstractmethod


class Type(ABC):
    @abstractmethod
    def match(self, o: Any, /) -> bool:
        raise NotImplementedError()


@dataclass
class IntType(Type):
    def __repr__(self) -> str:
        return "IntType()"

    def __str__(self) -> str:
        return "int"

    def match(self, o: Any, /) -> bool:
        return isinstance(o, int)


@dataclass
class FloatType(Type):
    def __repr__(self) -> str:
        return "FloatType()"

    def __str__(self) -> str:
        return "float"

    def match(self, o: Any, /) -> bool:
        return isinstance(o, float)


@dataclass
class StringType(Type):
    def __repr__(self) -> str:
        return "StringType()"

    def __str__(self) -> str:
        return "str"

    def match(self, o: Any, /) -> bool:
        return isinstance(o, str)


@dataclass
class BoolType(Type):
    def __repr__(self) -> str:
        return "BoolType()"

    def __str__(self) -> str:
        return "bool"

    def match(self, o: Any, /) -> bool:
        return isinstance(o, bool)


@dataclass
class ListType(Type):
    __slot__ = "_item_type"

    def __init__(self, item_type: Type, /) -> None:
        self._item_type = item_type

    def __repr__(self) -> str:
        return f"ListType({repr(self._item_type)})"

    def __str__(self) -> str:
        return f"[{self._item_type}]"

    def match(self, o: Any, /) -> bool:
        if not isinstance(o, list):
            return False

        if not self._item_type or not o:
            return True

        return self._item_type.match(o[0])


@dataclass
class TupleType(Type):
    __slot__ = "_items_types"

    def __init__(self, items_types: list[Type], /) -> None:
        self._items_types = list(items_types) if items_types is not None else []

    def __repr__(self) -> str:
        return f"TupleType({repr(self._items_types)})"

    def __str__(self) -> str:
        return f"({', '.join(map(str, self._items_types))})"

    def match(self, o: Any, /) -> bool:
        if not isinstance(o, tuple):
            return False

        if len(self._items_types) != len(o):
            return False

        return all((t.match(v) for t, v in zip(self._items_types, o)))


@dataclass
class UnionType(Type):
    __slot__ = "_items_types"

    def __init__(self, items_types: list[Type], /) -> None:
        self._items_types = list(items_types) if items_types is not None else []

    def __repr__(self) -> str:
        return f"UnionType({repr(self._items_types)})"

    def __str__(self) -> str:
        return " | ".join(map(str, self._items_types))

    def match(self, o: Any, /) -> bool:
        if not isinstance(o, tuple):
            return False

        if len(self._items_types) != len(o):
            return False

        return all((t.match(v) for t, v in zip(self._items_types, o)))


def typeof(o: Any, /) -> Type:
    r"""Get the type of a Python object.

    .. code-block:: python

        >>> from gada import typing
        >>> typing.typeof(True)
        BoolType()
        >>> typing.typeof(1)
        IntType()
        >>> typing.typeof("hello")
        StringType()
        >>> typing.typeof([[1]])
        ListType(ListType(IntType()))
        >>> typing.typeof((1, "hello"))
        TupleType([IntType(), StringType()])
        >>>

    :param o: Python object
    :return: it's type
    """
    if isinstance(o, bool):
        return BoolType()
    if isinstance(o, int):
        return IntType()
    if isinstance(o, float):
        return FloatType()
    if isinstance(o, str):
        return StringType()
    if isinstance(o, list):
        return ListType(typeof(o[0]) if o else None)
    if isinstance(o, tuple):
        return TupleType(map(typeof, o))

    raise Exception(f"unsupported type {type(o)}")
