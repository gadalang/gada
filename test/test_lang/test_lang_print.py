from gada import NodeCall
from gada.program import Context


def test_lang_print():
    cxt = Context([
        NodeCall(
            name="print",
            inputs={"in": "hello world"}
        )
    ])

    cxt.step()
    assert cxt.vars() == {}
