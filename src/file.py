import hashlib
from pathlib import Path
from typing import Self


class File:
    def __init__(self, path: Path):
        self.path = path
        with open(path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            self._hash = file_hash

    def __eq__(self, other: Self):
        return (self.path, self._hash) == (other.path, other._hash)

    def __hash__(self):
        return hash((self.path, self._hash))

    def __str__(self):
        data = [f"{self.__class__.__name__}: {self.path}"]
        return "\n".join(data)
