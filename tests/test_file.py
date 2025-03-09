import hashlib
import os
from pathlib import Path

import pytest

from sync.nodes import File


class TestFile:
    file_path = Path("./tests/test_hash.txt")

    @pytest.fixture(autouse=True)
    def work_with_test_file(self):
        with open(self.file_path, "w") as f:
            f.write("1")
        yield

        os.remove(self.file_path)

    def test_file_hash(self):
        file = File(self.file_path)
        assert file._hash == hashlib.sha256("1".encode()).hexdigest()

    def test_equal_files(self):
        assert File(self.file_path) == File(self.file_path)

    def test_chenged_files(self):
        file1 = File(self.file_path)
        with open(self.file_path, "w") as f:
            f.write("2")
        file2 = File(self.file_path)
        assert file1 != file2

    def test_set_with_equal_files(self):
        file1 = File(self.file_path)
        file2 = File(self.file_path)
        files = set((file1, file2))
        assert len(files) == 1

    def test_set_with_chenged_files(self):
        file1 = File(self.file_path)
        with open(self.file_path, "w") as f:
            f.write("2")
        file2 = File(self.file_path)
        files = set((file1, file2))
        assert len(files) == 2
