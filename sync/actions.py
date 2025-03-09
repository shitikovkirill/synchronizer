from abc import ABC, abstractmethod
from pathlib import Path
import shutil

from sync.nodes import Dir, Node
from typing import Type


class Action(ABC):
    @abstractmethod
    def __call__(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: {self.node}"

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.node)})"


class SingleNodeAction(Action, ABC):
    def __init__(self, node: Type[Node]):
        self.node = node


class Remove(SingleNodeAction):
    def __call__(self):
        if isinstance(self.node, Dir):
            self.node.path.rmdir()
        elif self.node.path.exists():
            self.node.path.unlink()


class Create(SingleNodeAction):
    def __call__(self):
        if isinstance(self.node, Dir):
            self.node.path.mkdir(parents=True, exist_ok=True)


class Copy(SingleNodeAction):
    def __call__(self):
        shutil.copy(self.node.abs_path, self.node.path)


class TowNodeAction(Action, ABC):
    def __init__(self, node: Type[Node], to: Type[Node]):
        self.node = node
        self.to = to

    def __repr__(self):
        return f"{self.__class__.__name__}(from={repr(self.node)}, to={repr(self.to)})"


class Move(TowNodeAction):
    def __call__(self):
        self.node.path.rename(self.to.path)
