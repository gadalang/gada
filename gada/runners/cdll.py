"""Official runner for C dlls.
"""
import os
from ctypes import *
from typing import List, Optional


def run(
    component, *, gada_config: dict, node_config: dict, argv: Optional[List] = None
):
    # Force module to be in node_path
    component_path = os.path.abspath(os.path.dirname(component.__file__))
    file_path = os.path.abspath(os.path.join(component_path, node_config["file"]))
    if not os.path.isfile(file_path):
        raise Exception("file {} not found".format(node_config["file"]))
    elif not file_path.startswith(component_path):
        raise Exception("can't run file outside of component directory")

    # Inherit from current env
    env = dict(os.environ)
    env.update(node_config.get("env", {}))

    lib = cdll.LoadLibrary(file_path)
    getattr(lib, node_config["entrypoint"])()
