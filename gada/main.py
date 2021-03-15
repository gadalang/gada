__all__ = ["run", "main"]
import os
import sys
import argparse
from typing import List, Tuple, Optional
from gada import component, loader


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


def run(command: str, options: Optional[List] = None):
    os.environ["GADAHOME"] = "F:/component-programming/gada"

    # Check command format
    args = command.split('.')
    if len(args) != 2:
        raise Exception("invalid command {}".format(command))

    # Load component module
    c = component.load(args[0])

    # Load node configuration
    config = component.get_node_config(
        component.load_config(c),
        args[1]
    )
    
    # Load correct runner
    if "runner" not in config:
        raise Exception("no configured runner")

    r = loader.load_runner(config["runner"])
    if not r:
        raise Exception("runner {} not found".format(config["runner"]))

    # Run component
    r.Runner().run(c, config, options)


def main(argv=None):
    argv = sys.argv if argv is None else argv

    parser = argparse.ArgumentParser(prog="Service", description="Help")
    parser.add_argument(
        "command", type=str, help="command name"
    )
    parser.add_argument(
        "options", type=str, nargs=argparse.REMAINDER, help="command options"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")
    args = parser.parse_args(args=argv[1:])
    options, additional_argv = split_unknown_args(args.options)

    run(
        command=args.command,
        options=options,
    )


if __name__ == "__main__":
    main(sys.argv)
