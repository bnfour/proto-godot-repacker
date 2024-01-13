#!/usr/bin/env python3

import argparse

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Allegedly working repacker for Godot resources, in a very blunt way.",
        epilog="Limitations exist, check the docs!")
    
    # TODO actual arguments for resources file and replacements folder

    return parser.parse_args()

def main(config: argparse.Namespace):

    # TODO a lot of things
    # check if the file to patch is actually a godot res file
    # for every file in replacements folder, do the replacement magic

    pass


if __name__ == "__main__":
    main(get_args())
