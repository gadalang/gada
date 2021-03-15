# coding: utf-8
from __future__ import annotations

__all__ = ["GadaTestCase"]
import sys
from typing import Any
import unittest


class GadaTestCase(unittest.TestCase):
    def test(self):
        pass


if __name__ == "__main__":
    unittest.main()
