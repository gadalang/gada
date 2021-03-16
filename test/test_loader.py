__all__ = ["LoaderTestCase"]
import os
import sys
import yaml
import unittest
from gada import loader


class LoaderTestCase(unittest.TestCase):
    def test_load(self):
        """Test loading python runner."""
        runner = loader.load_runner("python")

        self.assertTrue(hasattr(runner, "Runner"), "invalid module")

    def test_load_not_found(self):
        """Test loading invalid runner."""
        with self.assertRaises(Exception):
            loader.load_runner("invalid")


if __name__ == "__main__":
    unittest.main()
