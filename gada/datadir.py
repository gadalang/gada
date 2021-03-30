"""Manage data directory.
"""
# -*- coding: utf-8 -*-
from __future__ import annotations

__all__ = ["path", "load_config", "write_config"]
import os
import sys
import pathlib
import yaml


def path() -> pathlib.Path:
    """Get path to local data directory.

    * Windows: "AppData/Roaming/Gada"
    * Linux: ".local/share/gada"
    * Mac: "Library/Application Support/Gada"

    :return: path to local data directory
    """
    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData" / "Roaming" / "Gada"
    elif sys.platform == "linux":
        return home / ".local" / "share" / "gada"
    elif sys.platform == "darwin":
        return home / "Library" / "Application Support" / "Gada"


def load_config() -> dict:
    """Load ``{datadir}/config.yml`` configuration file.

    An empty configuration will be returned if an error occurs.

    :return: configuration
    """
    try:
        data_dir = path()

        with open(os.path.join(data_dir, "config.yml"), "r", encoding="utf-8") as f:
            return yaml.safe_load(f.read())
    except Exception as e:
        return {}


def write_config(config: dict = None):
    """Write ``{datadir}/config.yml`` configuration file.

    :return: configuration
    """
    data_dir = path()
    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, "config.yml"), "w", encoding="utf-8") as f:
        f.write(yaml.safe_dump(config))
