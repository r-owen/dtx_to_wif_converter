Convert FiberWorks dtx weaving pattern files to WIF 1.1

This runs as a command-line script written in Python. See Installation and Usage for instructions.

This package may also be used used to read dtx and wif files into a standard in-memory model (`dtx_to_wif.PatternData`). This may be used for writing weaving design or loom driver software.

This software is licensed under the MIT license; see license.text for details.

Installation
------------

Test if you have Python installed by running your [terminal application](#terminal-applications) and typing `python` at the command prompt. If this runs a Python interpreter and the displayed version is at least 3.7, then you are good to go.

If you don't already have Python installed, or your installed version is too old, download the free installer from python.org and run it. Then repeat the test above, to be sure the installation was successful.

Run the following terminal command to install the package:

`pip install dtx_to_wif`

The code is hosted on [github](https://github.com/r-owen/dtx_to_wif_converter). If you prefer to run from source, download the package, unpack it, cd to the source directory, and run: `pip install .`. (If you want to work on the software, or try it out without installing it, you can make a local "editable install" from downloaded source using `pip install -e .`).

Usage
-----

Run your [terminal application](#terminal-applications).

Type:

`dtx_to_wif path1 path2 ...`

where each `path` is the path to a .dtx file or a directory containing .dtx files. On macOS, if you drag a file or folder from Finder onto your Terminal, the path will be typed for you. Windows may well do the same thing with its file browser.

The program will scan each provided directory for files whose names end in ".dtx". This is a recursive search, meaning it looks in all directories inside the provided directory, no matter how deeply nested.

For each ".dtx" file the program finds, it will write a new WIF file in the same directory, with the same name and the ".wif" extension. If such a WIF file already exists, the program will warn you and not replace it. However, if you specify option `--overwrite` the program will overwrite (replace) existing WIF files.

Specify `--help` (or `-h`) to print help.

Note: on macOS or linux you can type `./dtx_to_wif` instead of `python dtx_to_wif`, but that is unlikely to work on Windows.

Terminal Applications
---------------------

The standard terminal applications are Terminal for macOS and Windows Terminal for Windows. There are other terminal applications available, but the standard ones will do just fine.

WIF Details
-----------

Known differences from the WIF files that FiberWorks writes:

- The default colors and separations for warp and weft may not match (this is just an internal detail; the resulting pattern is the same). This is because I have not figured out the algorithm FiberWorks uses to choose default colors and separations.
- The date the dtx file was created is not written to the WIF file, since WIF has no standard location for this information. FiberWorks saves it as a comment in the [TEXT] section ("; Creation ...").
