from __future__ import annotations
import os
from pathlib import Path
from typing import Any
import yaml
import pytest
import shutil
import functools
import gada
from gada import test_utils

TESTNODES_PATH: Path = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "testnodes")))
'''Absolute path to ``gada/test/testnodes``'''

CONFIG_PATH: Path = TESTNODES_PATH / "gada.yml"
'''Absolute path to ``testnodes/gada.yml``'''

PROG_PATH: Path = TESTNODES_PATH / "prog.yml"
'''Absolute path to ``testnodes/prog.yml``'''

GADA_CONFIG = {"bins": {}}
'''Empty configuration for gada'''

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

CONFIG_HELLO_NODE = {
    "nodes": [
        {"name": "hello", "bin": "python", "argv": r"${comp_dir}/__init__.py ${argv}"}
    ]
}


def _write_config(filename: str, config: dict) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w+") as f:
        f.write(yaml.safe_dump(config))

    assert os.path.exists(filename), "file not created"


def _load_config(filename: str) -> dict:
    with open(filename, "r") as f:
        return yaml.safe_load(f.read())


def write_gada_config(config: dict) -> None:
    """Overwrite gada config.

    :param config: new configuration
    """
    gada.datadir.write_config(config)


def write_module_config(config: dict) -> None:
    """Overwrite ``gada.yml`` with new config.

    :param config: new configuration
    """
    _write_config(CONFIG_PATH, config)


def load_module_config() -> dict:
    """Load ``gada.yml``.

    :return: configuration
    """
    return _load_config(CONFIG_PATH)


def write_prog_config(config: dict) -> None:
    """Overwrite ``prog.yml`` with new config.

    :param config: new configuration
    """
    with open(PROG_PATH, "w+") as f:
        f.write(yaml.safe_dump(config))


def del_module_config() -> None:
    CONFIG_PATH.unlink(missing_ok=True)
    assert not CONFIG_PATH.exists(), "file not deleted"


def del_prog_config() -> None:
    PROG_PATH.unlink(missing_ok=True)
    assert not PROG_PATH.exists(), "file not deleted"


def clean_test(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        del_module_config()
        del_prog_config()
        
        return fun(*args, **kwargs)

    return wrapper


def with_gada_config(_fun=None, config: dict=None):
    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            write_gada_config(GADA_CONFIG if config is None else config)
            return fun(*args, **kwargs)

        return wrapper

    return decorator if _fun is None else decorator(_fun)


def with_module_config(_fun=None, config: dict=None):
    def decorator(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            write_module_config(CONFIG_NO_NODES if config is None else config)
            return fun(*args, **kwargs)
        
        return wrapper

    return decorator if _fun is None else decorator(_fun)


@pytest.fixture
def module_config() -> dict:
    '''Load the configuration from ``gada.yml``.
    
    :return: configuration
    '''
    return load_module_config()


def main(
    argv: list[str] = None,
    *,
    has_stdout: bool = None,
    has_stderr: bool = None,
) -> tuple[str, str]:
    # Run gada node
    stdout, stderr = test_utils.run(argv)

    # Check outputs
    if has_stderr is False:
        assert stderr == "", "stderr should be empty"
    elif has_stderr is True:
        assert stderr != "", "stderr should not be empty"
    if has_stdout is False:
        assert stdout == "", "stdout should be empty"
    elif has_stdout is True:
        assert stdout != "", "stdout should not be empty"

    # Return outputs
    return stdout.strip(), stderr.strip()