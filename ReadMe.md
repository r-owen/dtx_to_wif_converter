Convert FiberWorks .dtx weaving pattern files to WIF 1.1

This software can also convert WeavePoint .wpo files to WIF, though it cannot read fiber thickness or spacing information, so the conversion loses information.

This runs as a command-line script written in Python. See Installation and Usage for instructions.

This package can also read .wif, .dtx, and .wpo files into a standard in-memory model (`dtx_to_wif.PatternData`).
This may be used for writing weaving design or loom driver software.

This software is licensed under the MIT license; see license.text for details.

Installation
------------

Test if you have Python installed by running your [terminal application](#terminal-applications) and typing `python` at the command prompt. If this runs a Python interpreter and the displayed version is at least 3.7, then you are good to go.

If you don't already have Python installed, or your installed version is too old, download the free installer from python.org and run it (on Windows you may want to get Python from the Microsoft Store). Then repeat the test above, to be sure the installation was successful.

Run the following terminal command to install the package:

`python -m pip install dtx_to_wif`

Watch the output carefully to see where it installs `dtx_to_wif` and `wpo_to_wif` (or, on Windows, `dtx_to_wif.exe` and `wpo_to_wif.exe`). On Windows these will be buried very deeply.

The code is hosted on [github](https://github.com/r-owen/dtx_to_wif_converter). If you prefer to run from source, download the package, unpack it, cd to the source directory, and run: `pip install .`. (If you want to work on the software, or try it out without installing it, you can make a local "editable install" from downloaded source using `pip install -e .`).

Usage
-----

Run your [terminal application](#terminal-applications).

Type the following on macOS or unix:

    dtx_to_wif path1 path2 ...  # on macOS or unix

If this fails, specify the path to `dtx_to_wif` (as shown in the output from python -m pip install), or add its directory to the PATH. Replace "dtx" with "wpo" to convert .wpo files.


On Windows type:

    <...path to dtx_to_wif...>dtx_to_wif.exe path1 path2 ...

where `<...path to dtx_to_wif...>` is the path to the file, as shown in the output from `python -m pip install`.

Each `path` argument is the path to a .dtx file or a directory (folder) containing .dtx files. On macOS, if you drag a file or folder from Finder onto your Terminal, the path will be typed for you.

The program will scan each provided directory for files whose names end in ".dtx". This is a recursive search, meaning it looks in all directories inside the provided directory, no matter how deeply nested.

For each ".dtx" file the program finds, it will write a new WIF file in the same directory, with the same name and the ".wif" extension. If such a WIF file already exists, the program will warn you and not replace it. However, if you specify option `--overwrite` the program will overwrite (replace) existing WIF files.

Specify `--help` (or `-h`) to print help.

Terminal Applications
---------------------

The standard terminal applications are "Terminal" for macOS, and "cmd.exe" for Windows. Other terminal applications are available, but the standard ones are fine.

Use in Other Software
---------------------

To read a weaving pattern of any supported type, call `read_pattern_file` (for a file on disk) or `read_pattern_data` (for data as a string).

To write wif pattern files call `write_wif`.

WIF Details
-----------

Known differences from the WIF files that FiberWorks writes:

- The default colors and separations for warp and weft may not match (this is just an internal detail; the resulting pattern is the same). This is because I have not figured out the algorithm FiberWorks uses to choose default colors and separations.
- The date the dtx file was created is not written to the WIF file, since WIF has no standard location for this information. FiberWorks saves it as a comment in the [TEXT] section ("; Creation ...").

Limitations
-----------

The WeavePoint .wpo reading code cannot read per-thread thickness or separation data.
Due to this limitation I consider `wpo_to_wif` only marginally useful.
The main use case for reading WeavePoint files is to support loom control software.
