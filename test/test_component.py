# coding: utf-8
from __future__ import annotations

__all__ = ["ComponentTestCase"]
import os
import sys
from typing import Any
import yaml
import unittest
from gada import component


PACKAGE_NAME = "gadalang_testnodes"
CONFIG_YML = os.path.join(os.path.dirname(__file__), PACKAGE_NAME, "config.yml")
CONFIG_NO_NODES = {"runner": "python"}
CONFIG_NODES = {"runner": "python", "nodes": {"echo": {"file": "__init__.py"}}}


class ComponentTestCase(unittest.TestCase):
    def _write_config(self, value):
        with open(CONFIG_YML, "w+") as f:
            f.write(yaml.safe_dump(value))

    def _remove_config(self):
        os.remove(CONFIG_YML)
        self.assertFalse(os.path.exists(CONFIG_YML), "config.yml not deleted")

    def _load_config(self):
        # Load component
        comp = component.load(PACKAGE_NAME)
        self.assertEquals(comp.__name__, PACKAGE_NAME, "invalid package returned")

        # Load component configuration
        return component.load_config(comp)

    def _write_config_and_load(self, value):
        self._write_config(value)
        return self._load_config()

    def test_load(self):
        """Test loading the gadalang_testnodes package that is in PYTHONPATH."""
        # Load component configuration
        config = self._write_config_and_load(CONFIG_NODES)

        self.assertEquals(config["runner"], "python", "incorrect configuration")

        # Get node configuration
        node_config = component.get_node_config(config, "echo")

        self.assertEquals(
            node_config["runner"], "python", "incorrect node configuration"
        )
        self.assertEquals(
            node_config["file"], "__init__.py", "incorrect node configuration"
        )

    def test_load_notfound(self):
        """Test loading a package that is not in the PYTHONPATH."""
        with self.assertRaises(Exception):
            comp = component.load("gadalang_invalid")

    def test_load_config(self):
        """Test loading config.yml file from gadalang_testnodes package."""
        config = self._write_config_and_load(CONFIG_NO_NODES)

        self.assertEquals(config, CONFIG_NO_NODES, "incorrect loaded configuration")

    def test_load_config_empty(self):
        """Test loading an existing but empty config.yml file."""
        with open(CONFIG_YML, "w+") as f:
            f.write("")

        config = self._load_config()

        self.assertIsNotNone(config, "invalid configuration")

    def test_load_config_notfound(self):
        """Test loading a non existing config.yml file."""
        self._remove_config()

        with self.assertRaises(Exception):
            component.load_config(sys)

    def test_get_node_config_no_nodes(self):
        """Test loading a config.yml file without nodes."""
        config = self._write_config_and_load(CONFIG_NO_NODES)

        with self.assertRaises(Exception):
            component.get_node_config(config, "echo")

    def test_get_node_config_notfound(self):
        """Test loading a config.yml file with unknown node."""
        config = self._write_config_and_load(CONFIG_NODES)

        with self.assertRaises(Exception):
            component.get_node_config(config, "invalid")


if __name__ == "__main__":
    unittest.main()
