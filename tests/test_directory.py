from pathlib import Path

import pytest

from sync.nodes import Dir


class Testdir:
    dir_path = Path("./tests/test_dir")

    @pytest.fixture(autouse=True)
    def work_with_test_dir(self):
        self.dir_path.mkdir(exist_ok=True)
        yield

        self.dir_path.rmdir()

    def test_equal_dir(self):
        assert Dir(self.dir_path) == Dir(self.dir_path)

    def test_chenged_dir(self):
        dir1 = Dir(self.dir_path)
        dir2 = Dir(self.dir_path / "fake")
        assert dir1 != dir2

    def test_set_with_equal_dir(self):
        dir1 = Dir(self.dir_path)
        dir2 = Dir(self.dir_path)
        dirs = set((dir1, dir2))
        assert len(dirs) == 1

    def test_set_with_chenged_dirs(self):
        dir1 = Dir(self.dir_path)
        dir2 = Dir(self.dir_path / "fake")
        dirs = set((dir1, dir2))
        assert len(dirs) == 2
