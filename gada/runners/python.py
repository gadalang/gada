"""Official runner for Python code.
"""
from typing import List, Optional
from gada.runners import generic


def run(
    component, *, gada_config: dict, node_config: dict, argv: Optional[List] = None
):
    generic.run(
        component=component,
        gada_config=gada_config,
        node_config={
            "bin": node_config.get("bin", "python"),
            "file": node_config["file"],
            "env": node_config.get("env", {}),
        },
        argv=argv,
    )
