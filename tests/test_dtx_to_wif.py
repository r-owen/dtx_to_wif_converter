import pathlib
import shutil
import subprocess
import tempfile
import unittest

rootdir = pathlib.Path(__file__).parent.parent
datadir = rootdir / "tests" / "data"


class TestDtxToWif(unittest.TestCase):
    def test_dtx_to_wif(self):
        cmdname = "dtx_to_wif"
        # Copy tests/data to a temp dir and run dtx_to_wif on the copied files,
        # to avoid writing files to tests/data
        with tempfile.TemporaryDirectory() as tempdirname:
            tempdir = pathlib.Path(tempdirname)
            for subdirname in ("basic_dtx", "desired_basic_wif"):
                shutil.copytree(datadir / subdirname, tempdir / subdirname)

            basic_dtx_dir = tempdir / "basic_dtx"
            basic_dtx_dir_str = basic_dtx_dir.as_posix()
            desired_basic_wif_dir = tempdir / "desired_basic_wif"
            result = subprocess.run(
                [cmdname, basic_dtx_dir_str], check=True, capture_output=True
            )
            self.check_run_result(result, desired_prefix="Writing")
            basic_dtx_paths = [path for path in basic_dtx_dir.rglob("*.dtx")]
            assert len(basic_dtx_paths) == 6
            for dtxpath in basic_dtx_paths:
                wifpath = dtxpath.with_suffix(".wif")
                assert wifpath.is_file()
                desired_basic_wif_path = desired_basic_wif_dir / wifpath.name
                self.assert_files_equal(wifpath, desired_basic_wif_path)

            # Clear the wif files in the basic_dtx dir tree and run again.
            # All wif files should be empty because they are not overwritten.
            for dtxpath in basic_dtx_paths:
                wifpath = dtxpath.with_suffix(".wif")
                with open(wifpath, "w") as f:
                    f.truncate()
            result = subprocess.run(
                [cmdname, basic_dtx_dir_str], check=True, capture_output=True
            )
            self.check_run_result(result, desired_prefix="Skipping")
            for dtxpath in basic_dtx_paths:
                wifpath = dtxpath.with_suffix(".wif")
                assert wifpath.is_file()
                with open(wifpath, "r") as f:
                    data = f.read()
                    assert data == ""

            # Check that --overwrite replaces the (currently empty) wif files
            # and check that individual files can be specified
            # (instead of, or in addition to, directories)
            filepathargs = [cmdname] + basic_dtx_paths + ["--overwrite"]
            result = subprocess.run(filepathargs, check=True, capture_output=True)
            self.check_run_result(result, desired_prefix="Overwriting")
            for dtxpath in basic_dtx_paths:
                wifpath = dtxpath.with_suffix(".wif")
                assert wifpath.is_file()
                desired_basic_wif_path = datadir / "desired_basic_wif" / wifpath.name
                self.assert_files_equal(wifpath, desired_basic_wif_path)

    def check_run_result(self, result, desired_prefix):
        """Check the result from running the function.

        Parameters:
        result: return value from subprocess.run_result,
                which must be configured to capture stderr and stdout
        desired_prefix: the desired beginning of each line of stdout
        """
        with self.subTest(result=result, desired_prefix=desired_prefix):
            assert result.returncode == 0
            assert result.stderr == b""
            for line in result.stdout.decode().split("\n"):
                if line:
                    assert line.startswith(desired_prefix)

    def assert_files_equal(self, path1, path2):
        with self.subTest(path1=path1, path2=path2):
            with open(path1, "r") as file1:
                data1 = file1.read()
            with open(path2, "r") as file2:
                data2 = file2.read()
            assert data1 == data2


if __name__ == "__main__":
    unittest.main()
