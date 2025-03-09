from collections import defaultdict
from pathlib import Path
from sync.tree import TreeBuilder


class TestTree:
    def test_empty_dir(self):
        builder = TreeBuilder(defaultdict(set))

        tree = builder.build(Path("./tests/dirs/empty"))
        assert str(tree) == "Dir: tests/dirs/empty"

    def test_simple_tree(self):
        builder = TreeBuilder(defaultdict(set))
        tree = builder.build(Path("./tests/dirs/simple"))
        assert (
            str(tree)
            == """
-- Dir: tests/dirs/simple
-- File: tests/dirs/simple/test.txt"""
        )

    def test_multi_tree(self):
        builder = TreeBuilder(defaultdict(set))
        tree = builder.build(Path("./tests/dirs/multi"))
        assert "tests/dirs/multi/1" in str(tree)
