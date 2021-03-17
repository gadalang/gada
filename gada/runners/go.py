"""Official runner for Go code.
"""
from typing import List, Optional
from gada.runners import generic


def run(
    comp, *, gada_config: dict, node_config: dict, argv: Optional[List] = None
):
    generic.run(
        comp=comp,
        gada_config=gada_config,
        node_config={
            "bin": node_config.get("bin", "go"),
            "command": r"${bin} run ${file} ${argv}",
            "file": node_config["file"],
            "env": node_config.get("env", {}),
        },
        argv=argv,
    )
