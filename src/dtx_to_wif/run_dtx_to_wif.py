__all__ = ["run_dtx_to_wif"]

import argparse
import pathlib
import traceback

from .dtx_reader import read_dtx
from .wif_writer import write_wif


def run_dtx_to_wif() -> None:
    """Command-line script to convert Fiberworks .dtx files to WIF format."""
    parser = argparse.ArgumentParser(
        description="Convert FiberWorks .dtx files to WIF files"
    )
    parser.add_argument(
        "inpath", nargs="+", help="dtx files or directories of files to parse"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="overwrite existing files?"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="print parsed data"
    )
    args = parser.parse_args()

    # We want to accept .dtx files as well as directory paths,
    # but path.rglob("*.dtx") returns nothing if path is a .dtx file.
    # Work around this by accumulating all file paths in advance.
    # Also purge duplicates while preserving order by using a dict
    # (we only need a set of paths, but set does not preserve order).
    infiles: dict[pathlib.Path, None] = dict()
    for infilestr in args.inpath:
        inpath = pathlib.Path(infilestr)
        if inpath.suffix == ".dtx":
            infiles[inpath] = None
        else:
            infiles.update((infile, None) for infile in inpath.rglob("*.dtx"))

    for infile in infiles:
        outfile = infile.with_suffix(".wif")
        if outfile.exists():
            if args.overwrite:
                print(f"Overwriting existing {outfile}")
            else:
                print(f"Skipping existing {outfile}")
                continue
        else:
            print(f"Writing {outfile}")

        try:
            with open(infile, "r") as f:
                pattern = read_dtx(f)
            with open(outfile, "w") as f:
                write_wif(f, pattern)
        except Exception:
            traceback.print_exc()
            print(f"Failed to write {outfile}")
            continue

        if args.verbose:
            print(pattern)
