import os
import yaml
import unittest
import gada
from gada import component


class TestCaseBase(unittest.TestCase):
    PACKAGE_NAME = "testnodes"
    FULL_PACKAGE_NAME = f"gadalang_{PACKAGE_NAME}"
    CONFIG_YML = os.path.join(
        os.path.dirname(__file__), FULL_PACKAGE_NAME, "config.yml"
    )
    CONFIG_NO_NODES = {"runner": "generic"}
    CONFIG_NO_RUNNER = {
        "nodes": {"helloworld": {"bin": "python", "file": "__init__.py"}}
    }
    CONFIG_UNKNOWN_RUNNER = {
        "runner": "unknown",
        "nodes": {"helloworld": {"bin": "python", "file": "__init__.py"}},
    }
    CONFIG_NODES = {
        "runner": "generic",
        "nodes": {"helloworld": {"bin": "python", "file": "__init__.py"}},
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

    def main(self, argv):
        return gada.main(["gada"] + argv)
