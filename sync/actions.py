from abc import ABC, abstractmethod
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
        if not self.node.path.exists():
            return

        if isinstance(self.node, Dir):
            shutil.rmtree(self.node.path)
        else:
            self.node.path.unlink()


class Create(SingleNodeAction):
    def __call__(self):
        if isinstance(self.node, Dir):
            self.node.path.mkdir(parents=True, exist_ok=True)
        else:
            raise NotImplementedError(f"Creation not implemented for this type {type(self.node)}")


class TowNodeAction(Action, ABC):
    def __init__(self, node: Type[Node], to: Type[Node]):
        self.node = node
        self.to = to

    def __str__(self):
        return f"{self.__class__.__name__}: from={repr(self.node)} to={repr(self.to)}"

    def __repr__(self):
        return f"{self.__class__.__name__}(from={repr(self.node)}, to={repr(self.to)})"


class Copy(TowNodeAction):
    def __init__(self, node: Type[Node], to: Type[Node] | None = None):
        super().__init__(node, to or node)

    def __call__(self):
        shutil.copy(self.node.abs_path, self.to.path)


class Move(TowNodeAction):
    def __call__(self):
        self.node.path.rename(self.to.path)
