# -*- coding: utf-8 -*-
__all__ = ["RunnerBase", "load"]
from abc import ABC, abstractmethod


class RunnerBase(ABC):
    """Base class for runners."""

    @abstractmethod
    def run(self, component, node_config, options):
        """Run a node.

        :param component: loaded component
        :param node_config: node configuration
        :param options: run options
        :return: outputs
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
