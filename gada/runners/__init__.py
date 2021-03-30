# -*- coding: utf-8 -*-
from __future__ import annotations

__all__ = ["run", "load"]
from typing import Optional


def run(
    comp,
    *,
    gada_config: dict,
    node_config: dict,
    argv: Optional[list[str]] = None,
    stdin=None,
    stdout=None,
    stderr=None
):
    """Run a node.

    :param comp: loaded component
    :param gada_config: gada configuration
    :param node_config: node configuration
    :param argv: additional CLI arguments
    :param stdin: input stream
    :param stdout: output stream
    :param stderr: error stream
    """
    raise NotImplementedError()


def load(name: str):
    """Load a runner registered in **gada.runners**.

    This will raise an exception if no runner is found.

    :param name: runner name
    :return: runner
    """
    import sys
    import pkgutil
    import importlib
    import pkg_resources
    import functools

    def iter_namespace(ns_pkg):
        for finder, _, ispkg in pkgutil.iter_modules(
            ns_pkg.__path__, ns_pkg.__name__ + "."
        ):
            yield _, functools.partial(importlib.import_module, _)
        for _ in pkg_resources.iter_entry_points("gada.runners"):
            yield "gada.runners.{}".format(_.name), _.load

    def normalize(name):
        return name[name.rfind(".") + 1 :]

    # sys.modules[__name__] == this module
    for _, load in iter_namespace(sys.modules[__name__]):
        if normalize(_) == name:
            return load()

    raise Exception("runner {} not found".format(name))
