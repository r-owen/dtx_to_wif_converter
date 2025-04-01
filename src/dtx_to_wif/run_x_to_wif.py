__all__ = ["run_dtx_to_wif", "run_wpo_to_wif"]

import argparse
import dataclasses
import pathlib
import traceback
from collections.abc import Callable
from typing import Any

from .dtx_reader import read_dtx
from .pattern_data import PatternData
from .wif_writer import write_wif
from .wpo_reader import read_wpo


@dataclasses.dataclass
class ReaderInfo:
    reader: Callable[[Any, str], PatternData]
    is_binary: bool
    program_name: str


# A dict of file suffix: ReaderInfo
Readers = {
    ".dtx": ReaderInfo(reader=read_dtx, is_binary=False, program_name="FiberWorks"),
    ".wpo": ReaderInfo(reader=read_wpo, is_binary=True, program_name="WeavePoint"),
}


def run_x_to_wif(suffix: str) -> None:
    """Command-line script to convert weaving pattern files to WIF format.

    Note: the readers all accept opened files instead of file paths to support
    data from a bytes or stream. For example base_loom_server receives
    pattern data as a bytes, rather than a file on disk.

    Parameters
    ----------
    suffix : str
        File suffix; must be one of the entries in Readers
    """
    if suffix not in Readers:
        raise NotImplementedError(
            f"Cannot read {suffix} files: must be one of {Readers.keys()}"
        )
    reader_info = Readers[suffix]
    parser = argparse.ArgumentParser(
        description=f"Convert {reader_info.program_name} {suffix} files to WIF files"
    )
    parser.add_argument(
        "inpath", nargs="+", help=f"{suffix} files or directories of files to parse"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="overwrite existing files?"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="print parsed data"
    )
    args = parser.parse_args()

    # We want to accept individual files as well as directory paths,
    # but path.rglob("*{suffix}") returns nothing if path is a file.
    # Work around this by accumulating all file paths in advance.
    # Also purge duplicates while preserving order by using a dict
    # (we only need a set of paths, but set does not preserve order).
    infiles: dict[pathlib.Path, None] = dict()
    for infilestr in args.inpath:
        inpath = pathlib.Path(infilestr)
        if inpath.suffix == suffix:
            infiles[inpath] = None
        else:
            infiles.update((infile, None) for infile in inpath.rglob(f"*{suffix}"))

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
            with open(infile, "rb" if reader_info.is_binary else "r") as inf:
                pattern = reader_info.reader(inf, infile.name)
            with open(outfile, "w") as outf:
                write_wif(outf, pattern)
        except Exception:
            traceback.print_exc()
            print(f"Failed to write {outfile}")
            continue

        if args.verbose:
            print(pattern)


def run_dtx_to_wif() -> None:
    run_x_to_wif(".dtx")


def run_wpo_to_wif() -> None:
    run_x_to_wif(".wpo")
