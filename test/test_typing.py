'''Tests on the ``gada.typing`` module'''
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
def test_match_bool():
    assert BOOL_TYPE.match(BOOL_VALUE)


@pytest.mark.typing
def test_match_int():
    assert INT_TYPE.match(INT_VALUE)


@pytest.mark.typing
def test_match_float():
    assert FLOAT_TYPE.match(FLOAT_VALUE)


@pytest.mark.typing
def test_match_string():
    assert STRING_TYPE.match(STRING_VALUE)


@pytest.mark.typing
def test_match_list():
    assert LIST_INT_TYPE.match(LIST_INT_VALUE)


@pytest.mark.typing
def test_match_tuple():
    assert TUPLE_INT_STRING_TYPE.match(TUPLE_INT_STRING_VALUE)
