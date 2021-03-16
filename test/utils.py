import os
import yaml
import unittest
import gada
from gada import component


class TestCaseBase(unittest.TestCase):
    PACKAGE_NAME = "gadalang_testnodes"
    CONFIG_YML = os.path.join(os.path.dirname(__file__), PACKAGE_NAME, "config.yml")
    CONFIG_NO_NODES = {"runner": "python"}
    CONFIG_NO_RUNNER = {
        "nodes": {"echo": {"file": "__init__.py", "entrypoint": "echo"}}
    }
    CONFIG_UNKNOWN_RUNNER = {
        "runner": "unknown",
        "nodes": {"echo": {"file": "__init__.py", "entrypoint": "echo"}},
    }
    CONFIG_NODES = {
        "runner": "python",
        "nodes": {"echo": {"file": "__init__.py", "entrypoint": "echo"}},
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
        self.assertEquals(
            comp.__name__, TestCaseBase.PACKAGE_NAME, "invalid package returned"
        )

        # Load component configuration
        return component.load_config(comp)

    def write_config_and_load(self, value):
        self.write_config(value)
        return self.load_config()

    def main(self, argv):
        return gada.main(["gada"] + argv)