
from pathlib import Path

from .directory import Dir
from .file import File

def tree_builder(root_path: Path):
    
    if root_path.is_dir():
        root_dir = Dir(root_path)
        dirs = root_path.iterdir()
        root_dir.inner = {tree_builder(dir) for dir in dirs}
        return root_dir

    elif root_path.is_file():
        return File(root_path)