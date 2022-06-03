"Package containing everything for running Gada programs."
__all__ = ["Context", "Program", "from_node", "load"]
import yaml
import re
from typing import Callable, Optional, Any, Union
from gada._model import Node, NodeCall, NodePath, NodeInstance, NodeNotFoundError
from gada import runners
from gada._log import logger


NodeLoader = Callable[[str], Node]
RunnerLoader = Callable[[str], Any]


VAR_REGEX = re.compile(r"^\s*\{\s*\{\s*(?P<id>\w+)(\.(?P<name>\w+))?\s*\}\s*\}\s*$")


class Context(object):
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
        r"""Context for running a list of nodes.

        :param steps: list of nodes
        :param parent: parent context
        :param vars: initial variables
        :param load_node: how to load nodes
        :param load_runner: how to load runners
        """
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
            else lambda name, cache: NodePath(name).load(cache=cache)
        )
        self._load_runner: RunnerLoader = (
            load_runner if load_runner is not None else runners.load
        )

    @property
    def parent(self) -> "Context":
        return self._parent

    @property
    def is_running(self) -> bool:
        return self._sp < len(self._steps)

    @property
    def is_done(self) -> bool:
        return not self.is_running

    @property
    def line(self) -> int:
        return self._steps[self._sp].line if self.is_running else 0

    def locals(self) -> dict:
        """Return the variables stored in this context"""
        return dict(self._vars)

    def vars(self) -> dict:
        """Return the variables accessible from this context"""
        return (self._parent.vars() if self._parent else {}) | self._vars

    def local(self, name: str, /) -> Any:
        """Return a local variable by name"""
        return self._vars.get(name, None)

    def var(self, name: str, /) -> Any:
        """Return a variable accessible from this context by name"""
        if name in self._vars:
            return self._vars[name]

        return self._parent.var(name) if self._parent else None

    def node(self, id: str, /) -> NodeInstance:
        """Get a node instance by id"""
        return self._node_instances.get(id, None)

    def step(self, *, cache: Optional[dict] = None) -> "Context":
        """Run the next node.

        :param cache: cache for storing many results
        """
        if self.is_done:
            return self

        step = self._steps[self._sp]
        logger.debug(f"run node {step.name} at line {step.line}...")

        try:
            node = self._load_node(step.name, cache=cache)
            logger.debug(f"node {node.name} loaded...")
        except NodeNotFoundError:
            raise Exception(f"node {step.name} not found at line {step.line}")

        cxt = self._run(node, step, cache=cache)
        self._sp = self._sp + 1
        return cxt

    def _run(
        self, node: Node, step: NodeCall, /, *, cache: Optional[dict] = None
    ) -> "Context":
        if node.is_pure:
            self._store(node, step, {})
            return self

        try:
            runner = self._load_runner(node.runner)
        except Exception:
            raise Exception(f"runner {node.runner} not found for node {node.name}")

        logger.debug(f"runner {node.runner} loaded...")

        inputs = self._gather_inputs(step)
        logger.debug(f"node inputs: {inputs}")
        outputs = runner.run(node=node, inputs=inputs, cache=cache)
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
            return self.node(id).var(name)

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
    __slot__ = ("_config", "_outputs", "_cache")

    def __init__(
        self, config: dict = None, /, *, name: str = None, steps: list[NodeCall] = None, inputs: Optional[list] = None, outputs: Optional[str] = None
    ) -> None:
        self._config = {
            "name": name if name is not None else "",
            "inputs": inputs if inputs is not None else [],
            "steps": steps if steps is not None else [],
        } | (config if config is not None else {})
        self._outputs = outputs
        self._cache: dict = {}

    @property
    def is_running(self) -> bool:
        return self._context.is_running

    @property
    def is_done(self) -> bool:
        return self._context.is_done

    @property
    def line(self) -> int:
        return self._context.line

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._config})"

    def step(self, inputs: Optional[dict] = None) -> Context:
        return Context(self._config["steps"], vars=inputs)

    def run(self, inputs: Optional[dict] = None) -> None:
        ctx = Context(self._config["steps"], vars=inputs)
        while not ctx.is_done:
            ctx = ctx.step(cache=self._cache)

        if self._outputs:
            return ctx.node(self._outputs).vars()


def from_node(node: Union[str, NodePath, Node], /) -> Program:
    r"""Wrap a single node as a runnable program.

    .. code-block:: python

        >>> from gada import program
        >>>
        >>> p = program.from_node("max")
        >>> p.run({"a": 1, "b": 2})
        {'out': 2}
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
        steps=[NodeCall(
            name=node.name,
            id="node",
            inputs={k["name"]: f'{{{{ {k["name"]} }}}}' for k in node.inputs}
        )]
    )


def load(file: str, /) -> Program:
    r"""Load a program from file.

    .. code-block:: python

        >>> from gada import program
        >>>
        >>> p = program.load("max.yml")
        >>> p.run({"a": 1, "b": 2})
        {'out': 2}
        >>>
    
    :param file: filename or filelike object
    :return: loaded program
    """
    if isinstance(file, str):
        with open(file, "r") as f:
            content = f.read()
    elif hasattr(file, "read"):
        content = file.read()
    else:
        raise Exception("argument must be a str or filelike object")

    return Program(yaml.safe_load(content))
