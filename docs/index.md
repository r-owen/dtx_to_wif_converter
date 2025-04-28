# dtx_to_wif

Convert FiberWorks .dtx and WeavePoint .wpo weaving pattern files to WIF 1.1.
You do not need a copy of FiberWorks or WeavePoint to use this software.

Conversion is done using a [terminal](#terminal-applications). If you are not comfortable using a terminal, this may not be the right package for you.

This package can also read .wif, .dtx, and .wpo files into an in-memory class, which is the same for all supported file formats.

## Converting Files

First [install](installing.md) the software.
Pay careful attention to where the `dtx_to_wif` and `wpo_to_wif` executables are installed.
The path will be long on Windows.

Run your [terminal application](#terminal-applications).

Type the following on macOS or unix:

    dtx_to_wif path1 path2 ...

If this fails, specify the path to `dtx_to_wif` (as shown when you installed the package), or add its directory to the PATH.

On Windows type:

    <...path to dtx_to_wif...>dtx_to_wif.exe path1 path2 ...

where `<...path to dtx_to_wif...>` is the path to the file, as shown when you installed `dtx_to_wif`.

The path arguments can files or directories.
All files in a directory are converted, as well as all subdirectories, sub-sub-directories, etc.

Replace "dtx" with "wpo" to convert WeavePoint .wpo files.

Each new WIF file is written to the same directory as the original file with the same file name but a ".wif" extension.
If a WIF file with that path already exists, the old file is left unchanged, with a warning.
To overwrite existing files, run the command with option `--overwrite`.

If you run the command with option `-h` you will see all available options.

## Reading Files Into Memory

This package can also read weaving pattern files into an in-memory representation, class `dtx_to_wif.PatternData`.
This could be used by dobby loom control software, pattern visualization software, or weaving design software.

To read a weaving pattern file that is in any supported format, call `dtx_to_wif.read_pattern_file(filepath)`.

To read a weaving pattern file from a string, call `dtx_to_wif.read_pattern_data(data: str, suffix: str, name: str)`.
Encode WeavePoint files, which are binary, as base64. The suffix must include a leading period, e.g. ".dtx".

To write `dtx_to_wif.PatternData` to a WIF file, call `write_wif`.

## Terminal Applications

The standard terminal applications are "Terminal" for macOS, and "cmd.exe" for Windows. Other terminal applications are available, but the standard ones are fine.

## Limitations

Known differences from the WIF files that FiberWorks writes:

* The date the dtx file was created is not written to the WIF file, since WIF has no standard location for this information.
  FiberWorks saves it as a comment in the [TEXT] section ("; Creation ...").
* The default colors and separations for warp and weft may not match.
  This is just an internal detail, as the resulting pattern is the same.
  (I have not figured out the algorithm FiberWorks uses to choose default colors and separations.)

The WeavePoint .wpo reader cannot read per-thread thickness or separation data.
Due to this limitation I consider `wpo_to_wif` only marginally useful.
The main use case for reading WeavePoint files is to support dobby loom control software.

## License

This software is licensed under the MIT license; see license.txt for details.
