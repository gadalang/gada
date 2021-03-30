# -*- coding: utf-8 -*-
"""Some utility tools used in tests.
"""
from __future__ import annotations

__all__ = ["PipeStream", "run", "testnodes_path", "write_testnodes_config"]
import os
import yaml
from typing import Optional
import gada


class PipeStream:
    """Create a safe pipe stream using ``os.pipe``:

    .. code-block:: python

        >>> import gada
        >>>
        >>> # Pipe will be closed when exiting the context
        >>> with gada.test_utils.PipeStream() as stream:
        ...     # Write to the pipe
        ...     stream.writer.write(b'hello')
        ...     stream.writer.close()
        ...
        ...     # Read from the same pipe
        ...     stream.reader.read()
        5
        b'hello'
        >>>

    The default behavior is to open the pipe in binary mode, meaning
    you need to write and read bytes arrays. But you can open the
    pipe in another mode with:

    .. code-block:: python

        >>> import gada
        >>>
        >>> # Open the pipe in text mode
        >>> with gada.test_utils.PipeStream(rmode="r", wmode="w") as stream:
        ...     # Can write text
        ...     stream.writer.write('hello')
        ...     stream.writer.close()
        ...
        ...     # Can read text
        ...     stream.reader.read()
        5
        'hello'
        >>>

    """

    def __init__(self, *, rmode=None, wmode=None, **kwargs):
        rmode = rmode if rmode is not None else "rb"
        wmode = wmode if wmode is not None else "wb"

        self._r, self._w = os.pipe()
        self._r, self._w = os.fdopen(self._r, rmode, **kwargs), os.fdopen(
            self._w, wmode, **kwargs
        )

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self._r.close()
        self._w.close()

    @property
    def reader(self):
        """Get a file object for the reader end.

        :return: reader end
        """
        return self._r

    @property
    def writer(self):
        """Get a file object for the writer end.

        :return: writer end
        """
        return self._w


def run(argv: Optional[list[str]] = None) -> tuple[str, str]:
    """Run a gada node and return a tuple ``(stdout, stderr)``:

    .. code-block:: python

        >> import gada
        >>
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
        >>> stdout, stderr = gada.test_utils.run(['testnodes.echo', 'hello'])
        >>> stdout.strip()
        'hello'
        >>>

    :param argv: CLI arguments
    :return: ``(stdout, stderr)`` tuple
    """
    argv = argv if argv is not None else []

    with PipeStream() as stdin:
        stdin.writer.close()

        with PipeStream() as stdout:
            with PipeStream() as stderr:
                gada.main(
                    ["gada"] + argv,
                    stdin=stdin.reader,
                    stdout=stdout.writer,
                    stderr=stderr.writer,
                )
                stdout.writer.close()
                stderr.writer.close()
                return (
                    stdout.reader.read().decode(errors="ignore"),
                    stderr.reader.read().decode(errors="ignore"),
                )


def testnodes_path() -> str:
    """Get the absolute path to ``gada/test/gadalang_testnodes``.

    :return: path to testnodes directory
    """
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "test", "gadalang_testnodes")
    )


def write_testnodes_config(config: dict):
    """Overwrite ``gada/test/gadalang_testnodes/config.yml``.

    :param config: new configuration
    """
    with open(os.path.join(testnodes_path(), "config.yml"), "w+") as f:
        f.write(yaml.safe_dump(config))
