import pathlib
import unittest

from dtx_to_wif import read_dtx, read_wif

rootdir = pathlib.Path(__file__).parent.parent
datadir = rootdir / "tests" / "data"
level1dir = datadir / "level1"
execpath = rootdir / "dtx_to_wif"


class TestWifReader(unittest.TestCase):
    def test_wif_reader(self):
        for dtx_file in level1dir.glob("*.dtx"):
            print(f"testing {dtx_file.stem}")
            wif_file = datadir / "expected wifs" / (dtx_file.stem + ".wif")
            with open(dtx_file, "r") as f:
                parsed_dtx = read_dtx(f)
            with open(wif_file, "r") as f:
                parsed_wif = read_wif(f)
            assert parsed_dtx == parsed_wif


if __name__ == "__main__":
    unittest.main()
