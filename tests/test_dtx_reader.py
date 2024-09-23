import pathlib
import unittest

import pytest

from dtx_to_wif import read_dtx

rootdir = pathlib.Path(__file__).parent.parent
bad_dtx_dir = rootdir / "tests" / "data" / "bad_dtx"


class TestDtxReader(unittest.TestCase):
    def test_read_bad_files(self):
        # Note: a few errors are not possible in dtx files,
        # since the data is in lists, not dicts. Test what we can.
        for dtx_file_path in bad_dtx_dir.rglob("*.dtx"):
            with self.subTest(file=dtx_file_path.name):
                with open(dtx_file_path, "r") as f:
                    with pytest.raises(RuntimeError):
                        read_dtx(f)


if __name__ == "__main__":
    unittest.main()
