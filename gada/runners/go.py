"""Official runner for Go code.
"""
import os
import subprocess
import importlib
from typing import List, Optional
from gada.runners import RunnerBase


class Runner(RunnerBase):
    def run(self, component, node_config: dict, options: Optional[List] = None):
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

        if "entrypoint" not in node_config:
            raise Exception("missing entrypoint in configuration")

        proc = subprocess.Popen(
            ["go", "run", file_path],
            env=env,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        stdouts, stderrs = proc.communicate()
