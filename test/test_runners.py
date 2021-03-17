__all__ = ["RunnersTestCase"]
import os
import sys
import yaml
import unittest
from gada import runners


class RunnersTestCase(unittest.TestCase):
    def test_load(self):
        """Test loading python runner."""
        runner = runners.load("generic")

        self.assertTrue(hasattr(runner, "run"), "invalid module")

    def test_load_not_found(self):
        """Test loading invalid runner."""
        with self.assertRaises(Exception):
            runners.load("invalid")


if __name__ == "__main__":
    unittest.main()
