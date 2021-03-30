.. -*- coding: utf-8 -*-
.. _writing:

Writing Gada Nodes
==================

.. code-block:: yaml

    nodes:
      echo:
        runner: generic
        bin: echo


.. code-block:: python

    >>> import gada
    >>> import gada.test_utils
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
    >>> # Need to create fake stdin and stdout for unittests
    >>> with gada.test_utils.PipeStream() as stdin:
    ...     with gada.test_utils.PipeStream() as stdout:
    ...         # Run node with CLI arguments
    ...         gada.main(
    ...             ['gada', 'testnodes.echo', 'hello'],
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
