import hashlib
import re
from pathlib import Path
from typing import DefaultDict, Self
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
    def __init__(self, path: Path, parrent: Self | None = None):
        self.path = path
        self.abs_path = path.absolute()
        self.parrent = parrent
        self.inner = set()

    def __eq__(self, other: Self):
        return self.path == other.path

    def __hash__(self):
        return hash(self.path)

    def __str__(self):
        data = []
        result = f"{self.__class__.__name__}: {self.path}"
        for item in self.inner:
            data.append(str(item))
            result += re.subn(r"(^|\n)", "\n-- ", "\n".join(data))[0]
        return result or "\n".join(data)

    def get_all_nodes(self):
        nodes = set([self])
        for item in self.inner:
            if isinstance(item, Dir):
                nodes.update(item.get_all_nodes())
            else:
                nodes.add(item)
        return nodes


class File(Node):
    def __init__(self, path: Path, parrent: Dir | None = None):
        self.path = path
        self.abs_path = path.absolute()
        self.parrent = parrent
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


class FileStorage(DefaultDict):
    def __init__(self):
        self.storage: DefaultDict[str, list] = DefaultDict(list)

    def clear(self):
        self.storage.clear()
