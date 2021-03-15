# -*- coding: utf-8 -*-
__all__ = ["load_plugin_modules"]
import pkgutil
import importlib
import pkg_resources
import functools
import gada.runners


def load_runner(name):
    def iter_namespace(ns_pkg):
        for finder, _, ispkg in pkgutil.iter_modules(
            ns_pkg.__path__, ns_pkg.__name__ + "."
        ):
            yield _, functools.partial(importlib.import_module, _)
        for _ in pkg_resources.iter_entry_points("gada.runners"):
            yield "gada.runners.{}".format(_.name), _.load

    def normalize(name):
        return name[name.rfind(".") + 1 :]

    for _, load in iter_namespace(gada.runners):
        if normalize(_) == name:
            return load()

    return None
