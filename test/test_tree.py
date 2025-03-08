

from pathlib import Path
from src.tree import tree_builder


class TestTree:
    def test_empty_dir(self):
        tree = tree_builder(Path("./test/dirs/empty"))
        assert str(tree) == "Dir: test/dirs/empty"
    
    def test_simple_tree(self):
        tree = tree_builder(Path("./test/dirs/simple"))
        assert str(tree) == '''
-- Dir: test/dirs/simple
-- File: test/dirs/simple/test.txt'''

    def test_multi_tree(self):
        tree = tree_builder(Path("./test/dirs/multi"))
        assert str(tree) == """
"""