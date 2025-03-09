from collections import defaultdict
from pathlib import Path

from sync.nodes import Dir
from sync.nodes import File


class TreeBuilder:
    def __init__(self, file_storage: defaultdict[str, set]):
        self.file_storage = file_storage

    def build(self, root_path: Path, parrent: Dir | None = None):

        if root_path.is_dir():
            root_dir = Dir(root_path, parrent)
            dirs = root_path.iterdir()
            root_dir.inner = {self.build(dir, root_dir) for dir in dirs}
            return root_dir

        elif root_path.is_file():
            file = File(root_path, parrent)
            self.file_storage[file._hash].add(file)
            return file
