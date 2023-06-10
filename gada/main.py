from __future__ import annotations

__all__ = ["run", "main"]
from typing import TYPE_CHECKING
import sys
import argparse
from gada import nodeutil, runners

if TYPE_CHECKING:
    from typing import Any


def split_unknown_args(argv: list[str]) -> tuple[list[str], list[str]]:
    """Separate known command-line arguments from unknown one.
    Unknown arguments are separated from known arguments by
    the special **--** argument.
    :param argv: command-line arguments
    :return: tuple (known_args, unknown_args)
    """
    for i in range(len(argv)):
        if argv[i] == "--":
            return argv[:i], argv[i + 1 :]

    return argv, []


def run(target: str, argv: list[str]) -> dict:
    """Run a Gada node or program.

    .. code-block:: python

        >>> import gada
        >>>
        >>> gada.run("max", {"a": 1, "b": 2})
        {'out': 2}
        >>>

    :param target: name of a node or path to a program
    :param argv: inputs passed to the node or program
    :return: node or program outputs
    """
    node = nodeutil.find_node(target)
    if not node:
        raise Exception(f"node {target} not found")

    parser = nodeutil.create_parser(node)
    args = parser.parse_args(args=argv)

    runner = runners.load(node.config.get("runner", "pymodule"))
    runner.run(node, inputs=vars(args))
    return {}


def list_packages() -> None:
    for package in nodeutil.iter_packages():
        print(package.name)


def list_node() -> None:
    for node in nodeutil.iter_nodes():
        print(node.config["name"])


def menu_callback(filenames, params: str) -> None:
    print(filenames)
    print(params)
    sys.stdin.read(1)


def main(
    argv: list[str] | None = None,
    *,
    stdin=None,
    stdout=None,
    stderr=None,
):
    """Gada main.

    :param argv: command line arguments
    :param stdin: input stream
    :param stdout: output stream
    :param stderr: error stream
    """
    parser = argparse.ArgumentParser(prog="gada", description="Help")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")
    subparsers = parser.add_subparsers(help="sub-command help", required=True)

    def parse_run(args):
        node_argv, gada_argv = split_unknown_args(args.argv)

        run(args.target, node_argv)

    def parse_list_package(args):
        list_packages()

    def parse_list_node(args):
        list_node()

    def parse_install(args):
        pass

    run_parser = subparsers.add_parser("run", help="run a gada node")
    run_parser.add_argument("target", type=str, help="gada node to run")
    run_parser.add_argument(
        "argv", type=str, nargs=argparse.REMAINDER, help="additional CLI arguments"
    )
    run_parser.set_defaults(func=parse_run)

    list_parser = subparsers.add_parser("list", help="list installed gada nodes")
    list_subparsers = list_parser.add_subparsers(help="sub-command help")

    list_package_parser = list_subparsers.add_parser(
        "package", help="list installed gada packages"
    )
    list_package_parser.set_defaults(func=parse_list_package)

    list_node_parser = list_subparsers.add_parser(
        "node", help="list installed gada nodes"
    )
    list_node_parser.set_defaults(func=parse_list_node)

    install_parser = subparsers.add_parser("install", help="install a gada node")
    install_parser.add_argument("target", type=str, help="gada node to install")
    install_parser.set_defaults(func=parse_install)

    args = parser.parse_args()
    args.func(args)
    # run(target=args.target, argv=node_argv, stdin=stdin, stdout=stdout, stderr=stderr)


if __name__ == "__main__":
    main()
