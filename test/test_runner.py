__all__ = ["RunnerTestCase"]
import os
import sys
import yaml
import unittest
from gada import loader


class RunnerTestCase(unittest.TestCase):
    def test_load(self):
        """Test loading python runner."""
        runner = loader.load_runner("python")

        self.assertTrue(hasattr(runner, "Runner"), "invalid module")

    def test_load_notfound(self):
        """Test loading invalid runner."""
        runner = loader.load_runner("invalid")

        self.assertIsNone(runner)


if __name__ == "__main__":
    unittest.main()
