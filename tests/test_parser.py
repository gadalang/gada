"""Tests on the ``gada.parser`` module"""
import pytest
from gada import typing
from gada import parser


def _assert_parse_type(s: str, t: typing.Type) -> None:
    assert parser.type(s) == t


@pytest.mark.parser
def test_parse_int():
    _assert_parse_type("int", typing.IntType())


@pytest.mark.parser
def test_parse_float():
    _assert_parse_type("float", typing.FloatType())


@pytest.mark.parser
def test_parse_float():
    _assert_parse_type(
        "(int, int, [[int | float]])",
        typing.TupleType(
            [
                typing.IntType(),
                typing.IntType(),
                typing.ListType(
                    typing.ListType(
                        typing.UnionType([typing.IntType, typing.FloatType])
                    )
                ),
            ]
        ),
    )
