Convert FiberWorks dtx handweaving files to WIF 1.1

This is a command-line script. To run it:

`$ ./dtx_to_wif path1 path2 ... --overwrite`

This will recursively scan each provided path (which may be a file or directory) for files whose names end in ".dtx". For each such file it finds, it will write a new WIF file in the same directory, with the standard ".wif" extension, provided such a file does not already exist. You can specify option `--overwrite` to (silently) overwrite existing WIF files.

Specify `--help` (or `-h`) to print help.

Known differences from the WIF files that FiberWorks writes:

- If no color information is given, this code writes a 2-element color table, whereas FiberWorks writes a much longer table.
- The warp/weft color sections specify the color of every end and every pick. By comparison, FiberWorks omits entries when the color is the default.
- The default color of weft (and possibly warp) yarns will likely not match FiberWorks's WIF files. I have not figured out the algorithm FiberWorks uses to pick a default weft color.

The script is written in Python 3 and uses only standard libraries.

This software is licensed under the MIT license; see license.text for details.
