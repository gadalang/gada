__all__ = ["MainTestCase"]
import os
import sys
import unittest
from .utils import TestCaseBase


class MainTestCase(TestCaseBase):
    def test_main(self):
        """Test calling main with a valid command."""
        # Write valid configuration
        self.write_config(TestCaseBase.CONFIG_NODES)

        # Call node
        self.main(["gadalang_testnodes.echo"])

    def test_main_invalid_command(self):
        """Test calling main with an invalid command."""
        # A valid command is component.node
        with self.assertRaises(Exception):
            self.main(["gadalang_testnodes"])

    def test_main_no_runner(self):
        """Test calling main without configured runner."""
        self.write_config(TestCaseBase.CONFIG_NO_RUNNER)

        with self.assertRaises(Exception):
            self.main(["gadalang_testnodes.echo"])

    def test_main_unknown_runner(self):
        """Test calling main with an unknown runner."""
        self.write_config(TestCaseBase.CONFIG_UNKNOWN_RUNNER)

        with self.assertRaises(Exception):
            self.main(["gadalang_testnodes.echo"])

    def test_main_remainder_args(self):
        """Test calling main with remainder args."""
        self.write_config(TestCaseBase.CONFIG_NODES)

        self.main(["gadalang_testnodes.echo", "a", "--", "b"])


if __name__ == "__main__":
    unittest.main()
