__all__ = ["run", "main"]
import os
import sys
import argparse
from typing import List, Tuple, Optional
from gada import component, runners, datadir


def split_unknown_args(argv: List) -> Tuple[List, List]:
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


def run(node: str, argv: Optional[List] = None):
    """Run a node.

    :param node: node to run
    :param argv: additional CLI arguments
    """
    # Load gada configuration
    gada_config = datadir.load_config()

    # Check command format
    node_argv = node.split(".")
    if len(node_argv) != 2:
        raise Exception(f"invalid command {node}")

    # Load component module
    comp = component.load(node_argv[0])

    # Load node configuration
    node_config = component.get_node_config(component.load_config(comp), node_argv[1])

    # Load correct runner
    runner = runners.load(node_config.get("runner", None))

    # Run component
    runner.run(comp=comp, gada_config=gada_config, node_config=node_config, argv=argv)


def main(argv=None):
    argv = sys.argv if argv is None else argv

    parser = argparse.ArgumentParser(prog="Service", description="Help")
    parser.add_argument("node", type=str, help="command name")
    parser.add_argument(
        "argv", type=str, nargs=argparse.REMAINDER, help="additional CLI arguments"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")
    args = parser.parse_args(args=argv[1:])
    node_argv, gada_argv = split_unknown_args(args.argv)

    run(node=args.node, argv=node_argv)


if __name__ == "__main__":
    main(sys.argv)
