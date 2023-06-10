"""Collection of nodes used in unittests.

PYTHONPATH will be automatically set so Python can find this package.
"""
import sys
import argparse


def main(argv):
    parser = argparse.ArgumentParser("hello")
    parser.add_argument("name", type=str, help="your name")
    args = parser.parse_args(argv[1:])

    print(f"hello {args.name} !")


if __name__ == "__main__":
    main(sys.argv)
