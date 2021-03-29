"""Generic runner that can run any command line.
"""
__all__ = ["get_bin_path", "get_command_format", "run"]
import os
import sys
import asyncio
import importlib
from typing import List, Optional
from gada import component


def get_bin_path(bin: str, *, gada_config: dict) -> str:
    """Get a binary path from gada configuration:

    .. code-block:: python

        >>> import os
        >>> import gada
        >>>
        >>> # Overwrite "{datadir}/config.yml"
        >>> with open(os.path.join(gada.datadir.path(), 'config.yml'), 'w+') as f:
        ...     f.write('''
        ...     bins:
        ...       python: /path/to/python
        ...     ''')
        45
        >>> # Load configuration
        >>> config = gada.datadir.load_config()
        >>> # Get path for "python" bin
        >>> gada.runners.generic.get_bin_path('python', gada_config=config)
        '/path/to/python'
        >>>

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
        '${bin} ${file} ${argv}'
        >>>

    :return: command format
    """
    return r"${bin} ${file} ${argv}"


def run(comp, *, gada_config: dict, node_config: dict, argv: Optional[List] = None):
    """Run a generic command:

    .. code-block:: python

        >>> import gada
        >>>
        >>> comp = gada.component.load('testnodes')
        >>> with open(os.path.join(gada.component.get_dir(comp), 'config.yml'), 'w+') as f:
        ...     f.write('''
        ...     nodes:
        ...       mynode:
        ...         runner: generic
        ...         bin: ls
        ...     ''')
        70
        >>> gada_config = gada.datadir.load_config()
        >>> comp_config = gada.component.load_config(comp)
        >>> print(comp_config)
        {'nodes': {'mynode': {'runner': 'generic', 'bin': 'ls'}}}
        >>> node_config = gada.component.get_node_config(comp_config, 'mynode')
        >>> print(node_config)
        {'runner': 'generic', 'cwd': None, 'env': {}, 'bin': 'ls'}
        >>> #gada.runners.generic.run(comp, gada_config=gada_config, node_config=node_config)
        >>>

    :param comp: loaded component
    :param gada_config: gada configuration
    :param node_config: node configuration
    :param argv: additional CLI arguments
    """
    argv = argv if argv is not None else []

    # Inherit from current env
    env = dict(os.environ)
    env.update(node_config.get("env", {}))

    if "bin" not in node_config:
        raise Exception("missing bin in configuration")

    bin_path = get_bin_path(node_config["bin"], gada_config=gada_config)

    command = node_config.get("command", get_command_format())
    command = command.replace(r"${bin}", bin_path)
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
            cwd=node_config.get("cwd", None),
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

    asyncio.run(_run_subprocess())
