import pathlib
import unittest

import pytest

from dtx_to_wif import read_dtx, read_wif

rootdir = pathlib.Path(__file__).parent.parent
datadir = rootdir / "tests" / "data"
basic_dtx_dir = datadir / "basic_dtx"
bad_wif_dir = datadir / "bad_dtx"


class TestWifReader(unittest.TestCase):
    def test_wif_reader_compared_to_dtx_reader(self):
        for dtx_path in basic_dtx_dir.glob("*.dtx"):
            with self.subTest(file=dtx_path.stem):
                wif_path = datadir / "desired_basic_wif" / (dtx_path.stem + ".wif")
                with open(dtx_path, "r") as f:
                    parsed_dtx = read_dtx(f)
                with open(wif_path, "r") as f:
                    parsed_wif = read_wif(f)
                assert parsed_dtx == parsed_wif

    def test_read_bad_files(self):
        for dtx_path_path in bad_wif_dir.rglob("*.wif"):
            with self.subTest(file=dtx_path_path.name):
                with open(dtx_path_path, "r") as f:
                    with pytest.raises(RuntimeError):
                        read_dtx(f)


if __name__ == "__main__":
    unittest.main()
