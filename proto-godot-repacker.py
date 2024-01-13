#!/usr/bin/env python3

import argparse
import os

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Allegedly working repacker for Godot resources, in a very blunt way.",
        epilog="Limitations exist, check the docs!")
    
    parser.add_argument("resfile", type=argparse.FileType("rb+"), help="Godot resource pack (.pck) or self-contained executable to patch")
    parser.add_argument("replacements_folder", type=dir_type, help="folder that holds replacement assets")

    return parser.parse_args()

def dir_type(path: str) -> str:
    """Checks that the provided path is a path to existing folder"""
    path = os.path.realpath(path)
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid folder name")

def main(config: argparse.Namespace):

    # TODO a lot of things
    # check if the file to patch is actually a godot res file
    # for every file in replacements folder, do the replacement magic

    pass


if __name__ == "__main__":
    main(get_args())
