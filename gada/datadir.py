"""Manage data directory.
"""
# -*- coding: utf-8 -*-
__all__ = ["path", "load_config"]
import os
import sys
import pathlib
import yaml


def path() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """
    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData" / "Roaming" / "Gada"
    elif sys.platform == "linux":
        return home / ".local" / "share" / "gada"
    elif sys.platform == "darwin":
        return home / "Library" / "Application Support" / "Gada"


def load_config():
    """Load configuration.

    An empty configuration will be returned if an error occurs.

    :return: configuration
    """
    try:
        data_dir = path()

        with open(os.path.join(data_dir, "config.yml")) as f:
            return yaml.safe_load(f.read())
    except Exception as e:
        return {}
