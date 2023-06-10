from gada.node import NodeCall
from gada.program import Context


def test_lang_print():
    cxt = Context(
        [NodeCall.from_config({"name": "print", "inputs": {"in": "hello world"}})]
    )

    cxt.step()
    assert cxt.vars() == {}
