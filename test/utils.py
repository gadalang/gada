# -*- coding: utf-8 -*-
from __future__ import annotations
import os
import yaml
import io
import unittest
import gada
from gada import component, test_utils


class TestCaseBase(unittest.TestCase):
    PACKAGE_NAME = "testnodes"
    FULL_PACKAGE_NAME = f"gadalang_{PACKAGE_NAME}"
    GADA_CONFIG = {"bins": {}}
    CONFIG_YML = os.path.join(
        os.path.dirname(__file__), FULL_PACKAGE_NAME, "config.yml"
    )
    CONFIG_NO_NODES = {"runner": "generic"}
    CONFIG_NO_RUNNER = {
        "nodes": {
            "hello": {"bin": "python", "argv": r"${comp_dir}/__init__.py ${argv}"}
        }
    }
    CONFIG_UNKNOWN_RUNNER = {
        "runner": "unknown",
        "nodes": {
            "hello": {"bin": "python", "argv": r"${comp_dir}/__init__.py ${argv}"}
        },
    }
    CONFIG_NODES = {
        "runner": "generic",
        "nodes": {
            "hello": {"bin": "python", "argv": r"${comp_dir}/__init__.py ${argv}"}
        },
    }

    def write_config(self, value):
        with open(TestCaseBase.CONFIG_YML, "w+") as f:
            f.write(yaml.safe_dump(value))

    def remove_config(self):
        os.remove(TestCaseBase.CONFIG_YML)
        self.assertFalse(
            os.path.exists(TestCaseBase.CONFIG_YML), "config.yml not deleted"
        )

    def load_config(self):
        # Load component
        comp = component.load(TestCaseBase.PACKAGE_NAME)
        self.assertEqual(
            comp.__name__, TestCaseBase.FULL_PACKAGE_NAME, "invalid package returned"
        )

        # Load component configuration
        return component.load_config(comp)

    def write_config_and_load(self, value):
        self.write_config(value)
        return self.load_config()

    def main(
        self,
        argv: list[str] = None,
        *,
        has_stdout: bool = None,
        has_stderr: bool = None,
    ) -> tuple[str, str]:
        # Run gada node
        stdout, stderr = test_utils.run(argv)

        # Check outputs
        if has_stderr is False:
            self.assertEqual(stderr, "", "should have no stderr")
        elif has_stderr is True:
            self.assertNotEqual(stderr, "", "should have stderr")
        if has_stdout is False:
            self.assertEqual(stdout, "", "should have no stdout")
        elif has_stdout is True:
            self.assertNotEqual(stdout, "", "should have stdout")

        # Return outputs
        return stdout.strip(), stderr.strip()
