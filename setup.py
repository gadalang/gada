from __future__ import annotations
from typing import TYPE_CHECKING
import io
import os
from setuptools import find_packages, setup

if TYPE_CHECKING:
    from typing import Any

install_requires = ["pyyaml", "jsonschema", "context_menu"]

extras_require = {
    "test": ["pytest", "pytest-html"],
}


def read(*filenames: str, **kwargs: Any) -> str:
    """Read contents of multiple files and join them together"""
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


pkg_info: dict[str, Any] = {}
exec(read("gada/__version__.py"), pkg_info)

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

setup(
    name="gada",
    version=pkg_info["__version__"],
    author=pkg_info["__author__"],
    author_email=pkg_info["__author_email__"],
    url=pkg_info["__url__"],
    project_urls={
        "Bug Tracker": "https://github.com/gadalang/gada/issues",
        "Source Code": "https://github.com/gadalang/gada/",
    },
    description="Python bridge to run code written in any language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    package_data={"gada": ["gada.yml", "gada.yml.schema"]},
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["gada = gada:main"],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
