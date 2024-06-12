import pathlib
import shutil
import subprocess
import tempfile
import unittest

rootdir = pathlib.Path(__file__).parent.parent
datadir = rootdir / "tests" / "data"
execpath = rootdir / "dtx_to_wif"


class TestDtxToWif(unittest.TestCase):
    def test_dtx_to_wif(self):
        assert execpath.is_file()
        with tempfile.TemporaryDirectory() as outdirname:
            print(f"{datadir=}, {outdirname=}")
            outdir = pathlib.Path(outdirname)
            shutil.copytree(datadir, outdir / "data")
            result = subprocess.run(
                [execpath, outdirname], check=True, capture_output=True
            )
            self.check_run_result(result, desired_prefix="Writing")
            dtxpaths = [path for path in outdir.rglob("*.dtx")]
            assert len(dtxpaths) == 4
            for dtxpath in dtxpaths:
                wifpath = dtxpath.with_suffix(".wif")
                assert wifpath.is_file()
                desired_wifpath = datadir / "expected wifs" / wifpath.name
                self.assert_files_equal(wifpath, desired_wifpath)

            # Clear the wif files and run again.
            # All wif files should be empty because they are not overwritten
            for dtxpath in dtxpaths:
                wifpath = dtxpath.with_suffix(".wif")
                with open(wifpath, "w") as f:
                    f.truncate()
            result = subprocess.run(
                [execpath, outdirname], check=True, capture_output=True
            )
            self.check_run_result(result, desired_prefix="Skipping")
            for dtxpath in dtxpaths:
                wifpath = dtxpath.with_suffix(".wif")
                assert wifpath.is_file()
                with open(wifpath, "r") as f:
                    data = f.read()
                    assert data == ""

            # Check that --overwrite replaces the (currently empty) wif files
            # and check that individual files can be specified, instead of directories
            filepathargs = [execpath] + dtxpaths + ["--overwrite"]
            result = subprocess.run(filepathargs, check=True, capture_output=True)
            self.check_run_result(result, desired_prefix="Overwriting")
            for dtxpath in dtxpaths:
                wifpath = dtxpath.with_suffix(".wif")
                assert wifpath.is_file()
                desired_wifpath = datadir / "expected wifs" / wifpath.name
                self.assert_files_equal(wifpath, desired_wifpath)

    def check_run_result(self, result, desired_prefix):
        """Check the result from running the function.

        Parameters:
        result: return value from subprocess.run_result,
                which must be configured to capture stderr and stdout
        desired_prefix: the desired beginning of each line of stdout
        """
        assert result.returncode == 0
        assert result.stderr == b""
        for line in result.stdout.decode().split("\n"):
            if line:
                assert line.startswith(desired_prefix)

    def assert_files_equal(self, path1, path2):
        with open(path1, "r") as file1:
            data1 = file1.read()
        with open(path2, "r") as file2:
            data2 = file2.read()
        assert data1 == data2


if __name__ == "__main__":
    unittest.main()
