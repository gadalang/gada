"""Tests on the ``gada.typing`` module"""
import pytest
from gada import typing


BOOL_VALUE = True
BOOL_TYPE = typing.BoolType()
INT_VALUE = 1
INT_TYPE = typing.IntType()
FLOAT_VALUE = 1.0
FLOAT_TYPE = typing.FloatType()
STRING_VALUE = "hello"
STRING_TYPE = typing.StringType()
LIST_INT_VALUE = [1]
LIST_INT_TYPE = typing.ListType(typing.IntType())
TUPLE_INT_STRING_VALUE = (1, "hello")
TUPLE_INT_STRING_TYPE = typing.TupleType([typing.IntType(), typing.StringType()])


def _assert_typeof(s: str, t: typing.Type) -> None:
    assert typing.typeof(s) == t


@pytest.mark.typing
def test_typeof_bool():
    _assert_typeof(BOOL_VALUE, BOOL_TYPE)


@pytest.mark.typing
def test_typeof_int():
    _assert_typeof(INT_VALUE, INT_TYPE)


@pytest.mark.typing
def test_typeof_float():
    _assert_typeof(FLOAT_VALUE, FLOAT_TYPE)


@pytest.mark.typing
def test_typeof_string():
    _assert_typeof(STRING_VALUE, STRING_TYPE)


@pytest.mark.typing
def test_typeof_list():
    _assert_typeof(LIST_INT_VALUE, LIST_INT_TYPE)


@pytest.mark.typing
def test_typeof_tuple():
    _assert_typeof(TUPLE_INT_STRING_VALUE, TUPLE_INT_STRING_TYPE)


@pytest.mark.typing
def test_isinstance_bool():
    assert typing.isinstance(BOOL_VALUE, BOOL_TYPE)


@pytest.mark.typing
def test_isinstance_int():
    assert typing.isinstance(INT_VALUE, INT_TYPE)


@pytest.mark.typing
def test_isinstance_float():
    assert typing.isinstance(FLOAT_VALUE, FLOAT_TYPE)


@pytest.mark.typing
def test_isinstance_string():
    assert typing.isinstance(STRING_VALUE, STRING_TYPE)


@pytest.mark.typing
def test_isinstance_list():
    assert typing.isinstance(LIST_INT_VALUE, LIST_INT_TYPE)


@pytest.mark.typing
def test_isinstance_tuple():
    assert typing.isinstance(TUPLE_INT_STRING_VALUE, TUPLE_INT_STRING_TYPE)
