from pathlib import Path
from unittest.mock import patch, mock_open

from sync.nodes import Dir, File

@patch("builtins.open", new_callable=mock_open, read_data="data".encode("utf-8"))
def test_node_str(file):
    dir1 = Dir(Path("test1"))
    dir2 = Dir(Path("test2"))
    file1 = File(Path("file3.txt"))
    dir1.inner.add(dir2)
    dir1.inner.add(file1)
    
    assert "-- File: file3.txt" in str(dir1)