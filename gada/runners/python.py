"""Official runner for Python code.
"""
import os
import importlib
from typing import List, Optional
from gada.runners import RunnerBase


class Runner(RunnerBase):
    def run(self, component, node_config: dict, options: Optional[List] = None):
        if "entrypoint" not in node_config:
            raise Exception("missing entrypoint in configuration")

        getattr(component, node_config["entrypoint"])()
