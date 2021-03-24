"""Official runner for generic code.
"""
import os
import sys
import asyncio
import importlib
from typing import List, Optional
from gada import component


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

        ${bin} ${file} ${argv}

    :return: command format
    """
    return r"${bin} ${file} ${argv}"


def run(comp, *, gada_config: dict, node_config: dict, argv: Optional[List] = None):
    """
    :param comp: loaded component
    :param gada_config: gada configuration
    :param node_config: node configuration
    :param argv: additional CLI arguments
    """
    argv = argv if argv is not None else []

    # Force module to be in node_path
    comp_path = component.get_dir(comp)
    file_path = os.path.abspath(os.path.join(comp_path, node_config["file"]))
    if not os.path.isfile(file_path):
        raise Exception(f"file {node_config['file']} not found")
    elif not file_path.startswith(comp_path):
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

    async def _pipe(_stdin, _stdout):
        """Pipe content of stdin to stdout until EOF.

        :param stdin: input stream
        :param stdout: output stream
        """
        while True:
            line = await _stdin.readline()
            if not line:
                return

            _stdout.buffer.write(line)
            _stdout.flush()

    async def _run_subprocess():
        """Run a subprocess."""
        proc = await asyncio.create_subprocess_shell(
            command,
            env=env,
            stdin=sys.stdin,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await asyncio.wait(
            [
                asyncio.create_task(_pipe(proc.stdout, sys.stdout)),
                asyncio.create_task(_pipe(proc.stderr, sys.stderr)),
                asyncio.create_task(proc.wait()),
            ],
            return_when=asyncio.ALL_COMPLETED,
        )

    asyncio.get_event_loop().run_until_complete(_run_subprocess())
