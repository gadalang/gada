'''Tests on the ``gada.program.Context`` class'''
from __future__ import annotations
from gada.node import Node, NodeCall, Param
from gada import program


CALL_NODE_A = NodeCall.from_config({
    "name": "A",
    "id": "a",
    "inputs": {
        "in": 1
    }
})

CALL_NODE_B = NodeCall.from_config({
    "name": "B",
    "id": "b",
    "inputs": {
        "in": "{{ a.out }}"
    }
})

def MockContext(steps: list[NodeCall]) -> program.Context:
    NODE_A = Node.from_config({
        "name": "A",
        "runner": "mock_runner",
        "inputs": [{"name": "in", "type": "int"}],
        "outputs": [{"name": "out", "type": "int"}]
    })

    NODE_B = Node.from_config({
        "name": "B",
        "runner": "mock_runner",
        "inputs": [{"name": "in", "type": "int"}],
        "outputs": [{"name": "out", "type": "int"}]
    })
    
    def run_a(inputs: dict) -> dict:
        return {"out": inputs.get("in", 0)}

    def run_b(inputs: dict) -> dict:
        return {"out": inputs.get("in", 0) + 1}

    NODES = {
        "A": (NODE_A, run_a),
        "B": (NODE_B, run_b)
    }

    class MockRunner():
        @staticmethod
        def run(node: Node, inputs: dict, **kwargs) -> dict:
            return NODES[node.name][1](inputs)

    def load_node(name, **_) -> Node:
        return NODES[name][0]

    def load_runner(name, **_):
        return MockRunner if name == "mock_runner" else None

    return program.Context(steps, load_node=load_node, load_runner=load_runner)


def test_context():
    cxt = MockContext([
        CALL_NODE_A,
        CALL_NODE_B
    ])

    assert cxt.vars() == {}
    assert not cxt.parent
    assert not cxt.node("a")
    assert not cxt.node("b")
    assert not cxt.is_done

    assert cxt.step() == cxt
    assert cxt.vars() == {"out": 1}
    assert cxt.node("a")
    assert cxt.node("a").outputs == {"out": 1}
    assert not cxt.node("b")
    assert not cxt.is_done

    assert cxt.step() == cxt
    assert cxt.vars() == {"out": 2}
    assert cxt.node("a")
    assert cxt.node("a").outputs == {"out": 1}
    assert cxt.node("b")
    assert cxt.node("b").outputs == {"out": 2}
    assert cxt.is_done
