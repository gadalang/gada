# -*- coding: utf-8 -*-
"""Generic runner that can run any command line.
"""
from __future__ import annotations

__all__ = ["get_bin_path", "get_command_format", "run"]
import os
import sys
import asyncio
import importlib
from typing import Optional
from gada import component


def get_bin_path(bin: str, *, gada_config: dict) -> str:
    """Get a binary path from gada configuration:

    .. code-block:: python

        >> import os
        >> import gada
        >>
        >> # Overwrite "{datadir}/config.yml"
        >> with open(os.path.join(gada.datadir.path(), 'config.yml'), 'w+') as f:
        ..     f.write('''
        ..     bins:
        ..       python: /path/to/python
        ..     ''')
        45
        >> # Load configuration
        >> config = gada.datadir.load_config()
        >> # Get path for "python" bin
        >> gada.runners.generic.get_bin_path('python', gada_config=config)
        '/path/to/python'
        >>

    If there is no custom path in gada configuration for this
    binary, then :py:attr:`bin` is returned.

    :param bin: binary name
    :param gada_config: gada configuration
    :return: binary path
    """
    return gada_config.get("bins", {}).get(bin, bin)


def get_command_format() -> str:
    r"""Get the generic command format for CLI:

    .. code-block:: python

        >>> import gada
        >>>
        >>> gada.runners.generic.get_command_format()
        '${bin} ${argv}'
        >>>

    :return: command format
    """
    return r"${bin} ${argv}"


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
    """Run a generic command:

    .. code-block:: python

        >>> import gada
        >>>
        >>> # Overwrite "gada/test/gadalang_testnodes/config.yml" for this test
        >>> gada.test_utils.write_testnodes_config({
        ...     'nodes': {
        ...         'echo': {
        ...             'runner': 'generic',
        ...             'bin': 'echo'
        ...         }
        ...     }
        ... })
        >>>
        >>> # Load "testnodes" component
        >>> comp = gada.component.load('testnodes')
        >>>
        >>> # Load component and node configuration
        >>> gada_config = gada.datadir.load_config()
        >>> comp_config = gada.component.load_config(comp)
        >>> print(comp_config)
        {'nodes': {'echo': {'bin': 'echo', 'runner': 'generic'}}}
        >>> node_config = gada.component.get_node_config(comp_config, 'echo')
        >>> print(node_config)
        {'runner': 'generic', 'cwd': None, 'env': {}, 'bin': 'echo'}
        >>>
        >>> # Need to create fake stdin and stdout for unittests
        >>> with gada.test_utils.PipeStream() as stdin:
        ...     with gada.test_utils.PipeStream() as stdout:
        ...         # Run node with CLI arguments
        ...         gada.runners.generic.run(
        ...             comp,
        ...             argv=['hello'],
        ...             gada_config=gada_config,
        ...             node_config=node_config,
        ...             stdin=stdin.reader,
        ...             stdout=stdout.writer,
        ...             stderr=stdout.writer
        ...         )
        ...
        ...         # Close writer end so we can read form it
        ...         stdout.writer.close()
        ...
        ...         # Read node output
        ...         stdout.reader.read().decode().strip()
        'hello'
        >>>

    :param comp: loaded component
    :param gada_config: gada configuration
    :param node_config: node configuration
    :param argv: additional CLI arguments
    :param stdin: input stream
    :param stdout: output stream
    :param stderr: error stream
    """
    argv = " ".join(argv) if argv is not None else ""
    stdin = stdin if stdin is not None else sys.stdin
    stdout = stdout if stdout is not None else sys.stdout.buffer
    stderr = stderr if stderr is not None else sys.stderr.buffer

    if "bin" not in node_config:
        raise Exception("missing bin in configuration")

    # Inherit from current env
    env = dict(os.environ)
    env.update(node_config.get("env", {}))

    bin_path = get_bin_path(node_config["bin"], gada_config=gada_config)

    command = node_config.get("command", get_command_format())
    command = command.replace(r"${bin}", bin_path)
    command = command.replace(
        r"${argv}",
        node_config["argv"].replace(r"${argv}", argv)
        if "argv" in node_config
        else argv,
    )
    command = command.replace(r"${comp_dir}", component.get_dir(comp))

    async def _pipe(_stdin, _stdout):
        """Pipe content of stdin to stdout until EOF.

        :param stdin: input stream
        :param stdout: output stream
        """
        while True:
            line = await _stdin.readline()
            if not line:
                return

            _stdout.write(line)
            _stdout.flush()

    async def _run_subprocess():
        """Run a subprocess."""
        proc = await asyncio.create_subprocess_shell(
            command,
            env=env,
            cwd=node_config.get("cwd", None),
            stdin=stdin,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await asyncio.wait(
            [
                asyncio.create_task(_pipe(proc.stdout, stdout)),
                asyncio.create_task(_pipe(proc.stderr, stderr)),
                asyncio.create_task(proc.wait()),
            ],
            return_when=asyncio.ALL_COMPLETED,
        )

    asyncio.run(_run_subprocess())
