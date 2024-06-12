Convert FiberWorks dtx handweaving files to WIF 1.1

This is a command-line script written in Python. See Installation and Usage for instructions.

This software is licensed under the MIT license; see license.text for details.

Installation
------------

Test if you have Python installed by running your [terminal application](#terminal-applications) and typing `python` at the command prompt. If this runs a Python interpreter and the displayed version is at least 3.6, then you are good to go.

If you don't already have Python installed, or your installed version is too old, download the free installer from python.org and run it. Then repeat the test above, to be sure the installation was successful.

Download this code, e.g. by going to https://github.com/r-owen/dtx_to_wif_converter/releases
Unpack the results and put the directory (or, if you prefer, just the file "dtx_to_wif") somewhere convenient, such as your home directory.

Usage
-----

Run your [terminal application](#terminal-applications).

Change directory to the directory containing `dtx_to_wif`.

Type:

`$ python dtx_to_wif path1 path2 ...`

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

- If no color information is given, this code writes a color table with only 2 entries. FiberWorks writes a much longer table.
- If the warp or weft has more than one color or separation, the associated section specifies a value for every end or pick. FiberWorks omits individual ends or picks that have the default value. I did this because I find WIF files easier to read if all color and separation data is in the same section.
- The default colors and separations for warp and weft may not match (but the colors and separations of each pick and end should match). This difference is due to the fact that I have not figured out the algorithm FiberWorks uses to generate default colors and separations.
