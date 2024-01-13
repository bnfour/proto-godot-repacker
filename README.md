# proto-godot-repacker
>it was easier to do this than to learn how to play sudoku with cats instead of numbers

A (scuffed) tool to replace assets in data used by games running Godot, with some conditions -- read below. Just enough for me, your mileage may vary.

## Disclaimers
- This is by no means a _complete_ packing tool. If you're desperate, it can be a starting point for one.
- All my knowledge about Godot prior to creating this was "this is the engine Brotato runs on".
- This script merely automates the thing I done in hex editor manually and it worked.
- See next section.

## Bold assumptions
This tool will work only if the following conditions are met:
- The replacement files are not bigger than original ones.  
This tool is too lazy to shift file contents, rewriting offsets all over the file. For my use case, original files I wanted to replace are loseless WEBPs, and the engine seems to load lossy images just fine, so it wasn't an issue.
- The files can survive being padded with zero bytes.  
True for at least WEBP images, haven't tried anything else.
- The file names are unique in the project, and everything is referenced via `res://.import/` folder.  
Was true in my case, but then again, I have zero understading of how exactly Godot resources work.

## Usage

Requirements: none, other than standard library.  
Tested on 3.12, most version restricting feature is probably typing.

```
python3 proto-godot-repacker.py -h
usage: proto-godot-repacker.py [-h] resfile replacements_folder

Allegedly working repacker for Godot resources, in a very blunt way.

positional arguments:
  resfile              Godot resource pack (.pck) or self-contained executable to patch IN-PLACE, remember to backup
  replacements_folder  folder that holds replacement assets

options:
  -h, --help           show this help message and exit

Limitations exist, check the docs!
```
`resfile` is a path to the file with resources to be replaced. It will be modified in-place, **make sure you have a backup!**

`replacements_folder` is a path to a folder with data on files to be replaced. The files should be named exactly as in resources. They should not be in any subfolder, directly in the replacements_folder. Any files not found in resources will be skipped with a warning.  
As an advice, mind the files: images I replaced were referred as and named as PNGs everywhere, but were in fact WEBP images.

### Getting the files to replace / unpacking
You can use https://github.com/tehskai/godot-unpacker to get original resources.

## Credits
This project is pretty much inspired by https://github.com/tehskai/godot-unpacker. It's source taught me ~~a lot~~ just enough about Godot resources.

Shoutout for Devcats' Sudocats for getting me interested in replacing resources in the first place (see quote at the top).

## License
BSD0. Do whatever, but remember it is provided "as is".
