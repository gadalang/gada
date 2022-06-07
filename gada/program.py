"Package containing everything for running Gada programs."
from __future__ import annotations

__all__ = ["NodeInstance", "Context", "Program", "from_node", "load"]
import yaml
import re
from dataclasses import dataclass
from typing import Callable, Optional, Any, Union
from pathlib import Path
from gada.node import Param, Node, NodeCall, NodePath, NodeNotFoundError
from gada import runners
from gada._log import logger


NodeLoader = Callable[[str], Node]
RunnerLoader = Callable[[str], Any]


VAR_REGEX = re.compile(r"^\s*\{\s*\{\s*(?P<id>\w+)(\.(?P<name>\w+))?\s*\}\s*\}\s*$")


@dataclass
class NodeInstance(object):
    """Instance of a node that has run.

    :param node: node definition
    :param step: call of that node from program
    :param outputs: outputs of that node
    """

    __slot__ = ("_node", "_step", "_outputs")

    def __init__(
        self, node: Node, step: NodeCall, /, outputs: Optional[dict] = None
    ) -> None:
        self._node: Node = node
        self._step: NodeCall = step
        self._outputs: dict = outputs if outputs is not None else {}

    @property
    def node(self) -> Node:
        """Node definition"""
        return self._node

    @property
    def step(self) -> NodeCall:
        """Call from the program"""
        return self._step

    @property
    def outputs(self) -> dict:
        """Outputs of the node"""
        return self._outputs


class Context(object):
    r"""Context storing the state of a running program.

    :param steps: list of nodes
    :param parent: parent context
    :param vars: initial global variables
    :param load_node: how to load nodes
    :param load_runner: how to load runners
    """
    __slots__ = (
        "_steps",
        "_parent",
        "_sp",
        "_vars",
        "_node_instances",
        "_load_node",
        "_load_runner",
    )

    def __init__(
        self,
        steps: list[NodeCall],
        /,
        *,
        parent: Optional["Context"] = None,
        vars: Optional[dict] = None,
        load_node: Optional[NodeLoader] = None,
        load_runner: Optional[RunnerLoader] = None,
    ) -> None:
        self._steps: list[NodeCall] = steps if steps is not None else []
        self._parent: Context = parent
        # stack pointer
        self._sp: int = 0
        # local variables not tied to any node
        self._vars: dict = vars if vars is not None else {}
        # instance of run nodes with results
        self._node_instances: dict[str, NodeInstance] = {}
        # loaders
        self._load_node: NodeLoader = (
            load_node
            if load_node is not None
            else lambda name: NodePath(name).load()
        )
        self._load_runner: RunnerLoader = (
            load_runner if load_runner is not None else runners.load
        )

    @property
    def parent(self) -> Optional["Context"]:
        """Parent context or **None**"""
        return self._parent

    @property
    def is_running(self) -> bool:
        """If there are nodes to run"""
        return self._sp < len(self._steps)

    @property
    def is_done(self) -> bool:
        """If all nodes have been run"""
        return not self.is_running

    @property
    def lineno(self) -> int:
        """Current line from the source code"""
        return self._steps[self._sp].lineno if self.is_running else 0

    def locals(self) -> dict:
        """Return the variables stored in this context"""
        return dict(self._vars)

    def vars(self) -> dict:
        """Return the variables stored in this context and the parent"""
        return (self._parent.vars() if self._parent else {}) | self._vars

    def local(self, name: str, /) -> Optional[Any]:
        """Return a variable from this context by name.

        :param name: name of a variable
        :return: it's value or **None**
        """
        return self._vars.get(name, None)

    def var(self, name: str, /) -> Optional[Any]:
        """Return a variable from this context or the parent by name.

        :param name: name of a variable
        :return: it's value or **None**
        """
        if name in self._vars:
            return self._vars[name]

        return self._parent.var(name) if self._parent else None

    def node(self, id: str, /) -> Optional[NodeInstance]:
        """Get the instance of a node that has run by it's unique id.

        :param id: unique node id
        :return: it's instance or **None**
        """
        return self._node_instances.get(id, None)

    def step(self) -> "Context":
        """Run the next node and stop.

        This function either returns **self** or a new node if running
        the node opens a new scope (i.e. branchs or loops).

        :return: **self** or a new context
        """
        if self.is_done:
            return self

        step = self._steps[self._sp]
        logger.debug(f"run node {step.name} at line {step.lineno}...")

        try:
            node = self._load_node(step.name)
            logger.debug(f"node {node.name} loaded...")
        except NodeNotFoundError as e:
            raise Exception(f"node {step.name} not found at line {step.lineno}") from e

        cxt = self._run(node, step)
        self._sp = self._sp + 1
        return cxt

    def _run(
        self, node: Node, step: NodeCall, /
    ) -> "Context":
        if node.is_pure:
            self._store(node, step, {})
            return self

        try:
            runner = self._load_runner(node.runner)
        except Exception as e:
            raise Exception(f"runner {node.runner} not found for node {node.name}") from e

        logger.debug(f"runner {node.runner} loaded...")

        inputs = self._gather_inputs(step)
        logger.debug(f"node inputs: {inputs}")
        outputs = runner.run(node=node, inputs=inputs)
        logger.debug(f"node outputs: {outputs}")
        self._store(node, step, outputs)
        return self

    def _gather_inputs(self, step: NodeCall, /) -> dict:
        def find_var(value):
            # the value can be a primitive type
            if not isinstance(value, str):
                return value

            # check if the value is a variable
            match = VAR_REGEX.match(value)
            if not match:
                return value

            id = match.group("id")
            name = match.group("name")
            if name is None:
                # direct variable
                return self.var(id)

            # node output
            return self.node(id).outputs.get(name, None)

        return {k: find_var(v) for k, v in step.inputs.items()}

    def _store(self, node: Node, step: NodeCall, /, outputs: dict) -> None:
        """Store results of step execution.

        If the node has an id set, it will be tracked by the context
        and be accessible via its id.

        If two nodes have the same id, the previously stored node will
        no longer be accessible.

        :param step: run step
        :param outputs: step results
        """
        self._vars.update(outputs)

        if step.id is not None:
            self._node_instances[step.id] = NodeInstance(node, step, outputs)


class Program(object):
    """A program formed of a list of nodes to run.

    :param steps: list of nodes
    :param name: program name
    :param inputs: program inputs
    :param outputs: unique id of a node from the program
    """

    __slot__ = ("_name", "_file", "_steps", "_inputs", "_outputs")

    def __init__(
        self,
        steps: list[NodeCall],
        *,
        name: Optional[str] = None,
        file: Optional[Path] = None,
        inputs: Optional[list[Param]] = None,
        outputs: Optional[str] = None,
    ) -> None:
        self._name: str = name
        self._file: Path = file
        self._steps: list[NodeCall] = list(steps) if steps is not None else []
        self._inputs: list[Param] = list(inputs) if inputs is not None else []
        self._outputs = outputs

    def step(self, inputs: Optional[dict] = None) -> Context:
        r"""Run a single step of the program.

        .. code-block:: python

            >>> from gada.program import Program
            >>>
            >>> p = Program.from_node("max")
            >>> ctx = p.step({"a": 1, "b": 2})
            >>> while not ctx.is_done:
            ...   ctx = ctx.step()
            ...
            >>>

        :param inputs: inputs passed to the program
        :return: a new context for running the program
        """
        return Context(self._steps, vars=inputs)

    def run(self, inputs: Optional[dict] = None) -> Optional[dict]:
        r"""Run the program until terminated and get its outputs.

        .. code-block:: python

            >>> from gada.program import Program
            >>>
            >>> p = Program.from_node("max")
            >>> p.run({"a": 1, "b": 2})
            {'out': 2}
            >>>

        :param inputs: inputs passed to the program
        :return: program outputs
        """
        ctx = Context(self._steps, vars=inputs)
        while not ctx.is_done:
            ctx = ctx.step()

        if self._outputs:
            return ctx.node(self._outputs).outputs

    @staticmethod
    def from_config(config: dict, /) -> Program:
        r"""Load a program from a JSON configuration.

        .. code-block:: python

            >>> from gada.program import Program
            >>>
            >>> Program.from_config({
            ...   "name": "min",
            ...   "inputs": [
            ...     {"name": "a", "type": "int"},
            ...     {"name": "b", "type": "int"}
            ...   ],
            ...   "steps": [
            ...     {"name": "min", "inputs": {"a": "{{ a }}", "b": "{{ b }}"}}
            ...   ]
            ... })
            ...
            <gada.program.Program ...>
            >>>

        :param config: configuration
        :return: loaded program
        """
        return Program(
            name=config.get("name", None),
            file=config.get("file", None),
            steps=[NodeCall.from_config(_) for _ in config.get("steps", [])],
            inputs=[Param.from_config(_) for _ in config.get("inputs", [])],
        )

    @staticmethod
    def from_node(node: Union[str, NodePath, Node], /) -> Program:
        r"""Wrap a single node as a runnable program.

        .. code-block:: python

            >>> from gada.program import Program
            >>>
            >>> Program.from_node("max")
            <gada.program.Program ...>
            >>>

        :param node: reference to a node
        :return: the node as a program
        """
        if isinstance(node, str):
            node = NodePath(node)

        if isinstance(node, NodePath):
            node = node.load()

        if not isinstance(node, Node):
            raise Exception("argument must be a str, NodePath, or Node")

        return Program(
            name=node.name,
            inputs=node.inputs,
            outputs="node",
            steps=[
                NodeCall(
                    name=node.name,
                    id="node",
                    inputs={k.name: f"{{{{ {k.name} }}}}" for k in node.inputs},
                )
            ],
        )

    @staticmethod
    def load(file: str, /) -> Program:
        r"""Load a program from file.

        .. code-block:: python

            >>> from gada.program import Program
            >>>
            >>> Program.load("max.yml")
            <gada.program.Program ...>
            >>>

        :param file: filename or filelike object
        :return: loaded program
        """
        if isinstance(file, str):
            path = Path(file)
            with open(file, "r") as f:
                content = f.read()
        elif hasattr(file, "read"):
            path = None
            content = file.read()
        else:
            raise Exception("argument must be a str or filelike object")

        return Program.from_config(yaml.safe_load(content) | {"file": path})
