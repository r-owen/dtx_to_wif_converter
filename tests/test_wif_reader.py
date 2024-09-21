import pathlib
import unittest

import pytest

from dtx_to_wif import read_dtx, read_wif

rootdir = pathlib.Path(__file__).parent.parent
datadir = rootdir / "tests" / "data"
basic_dtx_dir = datadir / "basic_dtx"
bad_wif_dir = datadir / "bad_dtx"


class TestWifReader(unittest.TestCase):
    def test_wif_reader(self):
        for prune in (False, True):
            for dtx_file in basic_dtx_dir.glob("*.dtx"):
                with self.subTest(file=dtx_file.stem, prune=prune):
                    wif_file = datadir / "desired_basic_wif" / (dtx_file.stem + ".wif")
                    with open(dtx_file, "r") as f:
                        parsed_dtx = read_dtx(f, prune=prune)
                    with open(wif_file, "r") as f:
                        parsed_wif = read_wif(f, prune=prune)
                    assert parsed_dtx == parsed_wif

    def test_read_bad_files(self):
        for prune in (False, True):
            for dtx_file_path in bad_wif_dir.rglob("*.wif"):
                with self.subTest(file=dtx_file_path.name, prune=prune):
                    with open(dtx_file_path, "r") as f:
                        with pytest.raises(RuntimeError):
                            read_dtx(f, prune=prune)


if __name__ == "__main__":
    unittest.main()
