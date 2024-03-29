#!/usr/bin/env python3

# scuffed tool, usage is limited, please please read
# https://github.com/bnfour/proto-godot-repacker

import argparse
import io
import hashlib
import mmap
import os
import struct
import sys
import typing

# region helper classes

class TypedConfigNamespace(object):
    """Helper class that wraps parsed arguments as implicit typed things,
    so the autocomplete and typechecking actually works"""
    def __init__(self, raw_args: argparse.Namespace) -> None:
        self.resfile: io.IOBase = raw_args.resfile
        self.replacements_folder: str = raw_args.replacements_folder

class ReplaceFileOptions(typing.NamedTuple):
    """Things we need to know about a resource in the file to replace it"""
    # actual file contents
    offset: int
    size: int
    # md5 hash that is stored directly after offset and size
    hash_offset: int

#endregion

#region argument parsing

def get_args() -> TypedConfigNamespace:
    parser = argparse.ArgumentParser(description="Allegedly working repacker for Godot resources, in a very blunt way.",
        epilog="Limitations exist, check the docs!")
    
    parser.add_argument("resfile", type=argparse.FileType("rb+"), help="Godot resource pack (.pck) or self-contained executable to patch IN-PLACE, remember to backup")
    parser.add_argument("replacements_folder", type=dir_type, help="folder that holds replacement assets")

    return TypedConfigNamespace(parser.parse_args())

def dir_type(path: str) -> str:
    """Checks that the provided path is a path to existing folder"""
    path = os.path.realpath(path)
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid folder name")

#endregion

# region file manipulating

def is_godot_resource(f: mmap.mmap) -> bool:
    magic = b"GDPC"
    if f.read(4) == magic:
        return True
    else:
        f.seek(-4, os.SEEK_END)
        return f.read(4) == magic

def try_to_find_resource(f: mmap.mmap, name: str) -> ReplaceFileOptions | None:
    to_search = b"res://.import/" + str.encode(name, "ascii")
    # we assume (incorrectly? works for me) that the first time file is mentioned, it's its header and not some import script
    index = f.find(to_search, 0)
    
    if index == -1:
        return None
    
    f.seek(index - 4)
    # determine the file name length to skip
    name_len = int.from_bytes(f.read(4), "little")
    f.seek(index + name_len)
    offset, size = struct.unpack_from("<QQ", f.read(8 + 8))
    md5_offset = f.tell()

    return ReplaceFileOptions(offset, size, md5_offset)

def replace_resource(f: mmap.mmap, new_content: bytes, options: ReplaceFileOptions) -> None:
    # no idea what the header does, just copy it as is
    f.seek(options.offset)
    original_header = f.read(0x20)
    
    # TODO header is the same, so why would we write and read it again?
    content = original_header + new_content
    if (len(content) > options.size):
        raise ValueError("Replacement file too big")
    
    # just pad with zeroes and hope it works
    content = content + b"\x00" * (options.size - len(content))
    f[options.offset:options.offset + options.size] = content
    
    # never checked what would happen if hash is not modified
    hash = bytes.fromhex(hashlib.md5(content).hexdigest())
    f[options.hash_offset:options.hash_offset + 16] = hash

#endregion

def main(config: TypedConfigNamespace):

    f = mmap.mmap(config.resfile.fileno(), 0)
    config.resfile.close()
    
    if not is_godot_resource(f):
        f.close()
        print("Input file does not look like a workable resource!")
        sys.exit(1)

    replacements = (asset for asset in os.listdir(config.replacements_folder) if os.path.isfile(os.path.join(config.replacements_folder, asset)))
    for file in replacements:
        full_path = os.path.join(config.replacements_folder, file)
        options = try_to_find_resource(f, file)
        if options is not None:
            with open(full_path, "rb") as replacement:
                content = replacement.read()
            try:
                replace_resource(f, content, options)
            except ValueError:
                print(f"{file}: replacement too big, unable to can")
        else:
            print(f"{file}: not found in file, skipping.")

    f.close()


if __name__ == "__main__":
    main(get_args())
