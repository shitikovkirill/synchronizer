import hashlib
import re
from pathlib import Path
from typing import Self
from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def __eq__(self, other: Self):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.path)})"


class Dir(Node):
    def __init__(self, path: Path):
        self.path = path
        self.inner = set()

    def __eq__(self, other: Self):
        return self.path == other.path

    def __hash__(self):
        return hash(self.path)

    def __str__(self):
        data = [f"{self.__class__.__name__}: {self.path}"]
        result = None
        for item in self.inner:
            data.append(str(item))
            result = re.subn(r"(^|\n)", "\n-- ", "\n".join(data))[0]
        return result or "\n".join(data)


class File(Node):
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