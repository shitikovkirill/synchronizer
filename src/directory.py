from pathlib import Path
import re
from typing import Self


class Dir:
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
