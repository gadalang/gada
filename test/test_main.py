__all__ = ["MainTestCase"]
import os
import sys
import logging
import unittest
import gada
from test.utils import TestCaseBase


class MainTestCase(TestCaseBase):
    def setUp(self):
        TestCaseBase.setUp(self)
        gada.datadir.write_config(TestCaseBase.GADA_CONFIG)

    def test_main(self):
        """Test calling main with a valid command."""
        # Write valid configuration
        self.write_config(TestCaseBase.CONFIG_NODES)

        # Call node
        stdout, stderr = self.main(
            ["testnodes.hello", "john"], has_stdout=True, has_stderr=False
        )

        # Node should return "hello john !"
        self.assertEqual(stdout, "hello john !", "wrong output")

    def test_main_remainder_args(self):
        """Test calling main with remainder args."""
        self.write_config(TestCaseBase.CONFIG_NODES)

        stdout, stderr = self.main(
            ["testnodes.hello", "john", "--", "b"], has_stdout=True, has_stderr=False
        )

        # Node should return "hello john !"
        self.assertEqual(stdout, "hello john !", "wrong output")

    def test_main_help(self):
        """Test calling main to display help."""
        self.write_config(TestCaseBase.CONFIG_NODES)

        stdout, stderr = self.main(
            ["testnodes.hello"], has_stdout=False, has_stderr=True
        )

        # Node should output argparse help
        self.assertIn("usage: hello [-h]", stderr, "wrong output")

    def test_main_invalid_command(self):
        """Test calling main with an invalid command."""
        # A valid command is component.node
        with self.assertRaises(Exception):
            self.main(["testnodes"])

    def test_main_no_runner(self):
        """Test calling main without configured runner."""
        self.write_config(TestCaseBase.CONFIG_NO_RUNNER)

        with self.assertRaises(Exception):
            self.main(["testnodes.hello"])

    def test_main_unknown_runner(self):
        """Test calling main with an unknown runner."""
        self.write_config(TestCaseBase.CONFIG_UNKNOWN_RUNNER)

        with self.assertRaises(Exception):
            self.main(["testnodes.hello"])


if __name__ == "__main__":
    unittest.main()
