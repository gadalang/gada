"""Tests on the ``gada.Node`` class"""
import pytest
from gada import node
import conftest


@conftest.clean_test
@conftest.with_module_config(config=conftest.CONFIG_NO_RUNNER)
def test_nodes():
    """Test getting nodes from ``test.testnodes``"""
    assert (
        node.nodes("test.testnodes") == conftest.CONFIG_NO_RUNNER["nodes"]
    ), "invalid nodes"
