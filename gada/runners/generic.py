"""Official runner for generic code.
"""
import os
import subprocess
import importlib
from typing import List, Optional


def get_bin_path(bin: str, *, gada_config: dict) -> str:
    """Get a binary path from gada configuration.

    If there is no custom path in gada configuration for this
    binary, then :py:attr:`bin` is returned.

    :param bin: binary name
    :param gada_config: gada configuration
    :return: binary path
    """
    return gada_config.get("bins", {}).get(bin, bin)


def get_command_format() -> str:
    """Get the generic command format for CLI.

    The default format is:

    .. code-block:: bash

        ${bin} ${file} ${args}

    :return: command format
    """
    return r"${bin} ${file} ${args}"


def run(
    component, *, gada_config: dict, node_config: dict, argv: Optional[List] = None
):
    """
    :param component: parent component
    :param gada_config: gada configuration
    :param node_config: node configuration
    :param argv: additional CLI arguments
    """
    argv = argv if argv is not None else []

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

    if "bin" not in node_config:
        raise Exception("missing bin in configuration")

    bin_path = get_bin_path(node_config["bin"], gada_config=gada_config)

    command = node_config.get("command", get_command_format())
    command = command.replace(r"${bin}", bin_path)
    command = command.replace(r"${file}", file_path)
    command = command.replace(r"${argv}", " ".join(argv))

    proc = subprocess.Popen(
        command, env=env, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )

    stdouts, stderrs = proc.communicate()
