#!/usr/bin/env python3

import argparse
import io
import mmap
import os
import sys

class TypedConfigNamespace(object):
    """Helper class that wraps parsed arguments as implicit typed things,
    so the autocomplete and typechecking actually works"""
    def __init__(self, raw_args: argparse.Namespace) -> None:
        self.resfile: io.IOBase = raw_args.resfile
        self.replacements_folder: str = raw_args.replacements_folder

def get_args() -> TypedConfigNamespace:
    parser = argparse.ArgumentParser(description="Allegedly working repacker for Godot resources, in a very blunt way.",
        epilog="Limitations exist, check the docs!")
    
    parser.add_argument("resfile", type=argparse.FileType("rb+"), help="Godot resource pack (.pck) or self-contained executable to patch")
    parser.add_argument("replacements_folder", type=dir_type, help="folder that holds replacement assets")

    return TypedConfigNamespace(parser.parse_args())

def dir_type(path: str) -> str:
    """Checks that the provided path is a path to existing folder"""
    path = os.path.realpath(path)
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid folder name")

def is_godot_resource(f: mmap.mmap) -> bool:
    magic = b"GDPC"
    if f.read(4) == magic:
        f.seek(0)
        return True
    else:
        f.seek(-4, os.SEEK_END)
        if f.read(4) == magic:
            return True
        return False


def main(config: TypedConfigNamespace):

    f = mmap.mmap(config.resfile.fileno(), 0)
    config.resfile.close()
    
    if not is_godot_resource(f):
        f.close()
        print("Input file does not look like a workable resource!")
        sys.exit(1)

    replacements = (asset for asset in os.listdir(config.replacements_folder) if os.path.isfile(os.path.join(config.replacements_folder, asset)))
    for file in replacements:
        print(f"Replacing of {file} goes here")
        # TODO rapid action

    f.close()


if __name__ == "__main__":
    main(get_args())
