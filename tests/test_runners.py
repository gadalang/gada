import pytest
from gada import runners


def test_load():
    """Test loading python runner."""
    runner = runners.load("generic")

    assert hasattr(runner, "run"), "invalid module"


def test_load_not_found():
    """Test loading invalid runner."""
    with pytest.raises(Exception):
        runners.load("invalid")
