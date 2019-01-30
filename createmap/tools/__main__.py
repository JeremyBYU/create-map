#!/usr/bin/env python3

import argparse

from createmap.tools import np2las, npfilt, np2geom, npjoin

def add_parsers():
    parser = argparse.ArgumentParser(prog="./cv")
    subparser = parser.add_subparsers(title="createmap", metavar="")

    # Add your tool's entry point below.
    np2las.add_parser(subparser)
    npfilt.add_parser(subparser)
    np2geom.add_parser(subparser)
    npjoin.add_parser(subparser)


    # We return the parsed arguments, but the sub-command parsers
    # are responsible for adding a function hook to their command.
    return parser.parse_args()


if __name__ == "__main__":
    args = add_parsers()
    args.func(args)