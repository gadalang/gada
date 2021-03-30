__all__ = ["ComponentTestCase"]
import os
import sys
import yaml
import unittest
from gada import component
from test.utils import TestCaseBase


class ComponentTestCase(TestCaseBase):
    def test_load(self):
        """Test loading the gadalang_testnodes package that is in PYTHONPATH."""
        # Load component configuration
        config = self.write_config_and_load(TestCaseBase.CONFIG_NODES)

        self.assertEqual(config["runner"], "generic", "incorrect configuration")

        # Get node configuration
        node_config = component.get_node_config(config, "hello")

        self.assertEqual(
            node_config["runner"], "generic", "incorrect node configuration"
        )
        self.assertEqual(node_config["bin"], "python", "incorrect node configuration")
        self.assertEqual(
            node_config["argv"],
            r"${comp_dir}/__init__.py ${argv}",
            "incorrect node configuration",
        )

    def test_load_not_found(self):
        """Test loading a package that is not in the PYTHONPATH."""
        with self.assertRaises(Exception):
            comp = component.load("gadalang_invalid")

    def test_load_config(self):
        """Test loading config.yml file from gadalang_testnodes package."""
        config = self.write_config_and_load(TestCaseBase.CONFIG_NO_NODES)

        self.assertEqual(
            config, TestCaseBase.CONFIG_NO_NODES, "incorrect loaded configuration"
        )

    def test_load_config_empty(self):
        """Test loading an existing but empty config.yml file."""
        with open(TestCaseBase.CONFIG_YML, "w+") as f:
            f.write("")

        config = self.load_config()

        self.assertIsNotNone(config, "invalid configuration")

    def test_load_config_not_found(self):
        """Test loading a non existing config.yml file."""
        self.remove_config()

        with self.assertRaises(Exception):
            component.load_config(sys)

    def test_get_node_config_not_found(self):
        """Test loading a config.yml file with unknown node."""
        config = self.write_config_and_load(TestCaseBase.CONFIG_NODES)

        with self.assertRaises(Exception):
            component.get_node_config(config, "invalid")


if __name__ == "__main__":
    unittest.main()
