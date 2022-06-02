import gada
from test.utils import TestCaseBase
from conftest import (
    PROG_PATH,
    clean_test,
    with_gada_config,
    with_module_config,
    main,
)


@clean_test
@with_gada_config
@with_module_config
def test_main():
    """Test calling main with a valid command."""
    # Run prog.yml
    stdout, _ = main(
        [PROG_PATH], has_stdout=True, has_stderr=False
    )

    # Node should return "hello john !"
    assert stdout == "hello john !", "wrong output"


def test_main_remainder_args(self):
    """Test calling main with remainder args."""
    self.write_config(TestCaseBase.CONFIG_NODES)

    stdout, stderr = self.main(
        ["testnodes.hello", "john", "--", "b"], has_stdout=True, has_stderr=False
    )

    # Node should return "hello john !"
    self.assertEqual(stdout, "hello john !", "wrong output")

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
