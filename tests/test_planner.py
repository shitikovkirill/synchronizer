from collections import defaultdict
from pathlib import Path
from sync.actions import Copy, Remove
from sync.planner import ActionOptimaser, Syncronisator
from sync.nodes import Dir, File
from unittest.mock import patch, mock_open


class TestPlaner:
    def test_get_diff(self):
        dir1 = Dir(Path("test1"))
        dir2 = Dir(Path("test2"))
        sync = set((dir1,))
        repl = set((dir2,))

        need_add = sync.difference(repl)

        assert need_add == set((dir1,))

    def test_get_plann_wirh_diff(self):
        dir1 = Dir(Path("test1"))
        dir2 = Dir(Path("test2"))
        sync = set((dir1,))
        repl = set((dir2,))
        syncr = Syncronisator(ActionOptimaser(defaultdict(set), defaultdict(set)))
        plan = syncr.get_diff(sync, repl)

        assert len(plan) == 2
        assert repr(plan[0]) == "Remove(Dir(PosixPath('test2')))"
        assert repr(plan[1]) == "Copy(Dir(PosixPath('test1')))"

    def test_get_plann_wirh_same(self):
        dir1 = Dir(Path("test1"))
        dir2 = Dir(Path("test1"))
        sync = set((dir1,))
        repl = set((dir2,))
        syncr = Syncronisator(ActionOptimaser(defaultdict(set), defaultdict(set)))
        plan = syncr.get_diff(sync, repl)

        assert len(plan) == 0

    def test_get_plann_wirh_same_file(self):
        with patch(
            "builtins.open", mock_open(read_data="1".encode("utf-8"))
        ) as mock_file:
            file1 = File(Path("test1"))
            file2 = File(Path("test1"))
        sync = set((file1,))
        repl = set((file2,))
        syncr = Syncronisator(ActionOptimaser(defaultdict(set), defaultdict(set)))
        plan = syncr.get_diff(sync, repl)

        assert len(plan) == 0

    def test_get_plann_wirh_diff_file(self):
        with patch(
            "builtins.open", mock_open(read_data="1".encode("utf-8"))
        ) as mock_file:
            file1 = File(Path("test1"))
        with patch(
            "builtins.open", mock_open(read_data="2".encode("utf-8"))
        ) as mock_file:
            file2 = File(Path("test1"))
        sync = set((file1,))
        repl = set((file2,))
        syncr = Syncronisator(ActionOptimaser(defaultdict(set), defaultdict(set)))
        plan = syncr.get_diff(sync, repl)

        assert len(plan) == 2

    @patch("builtins.open", new_callable=mock_open, read_data="data".encode("utf-8"))
    def test_get_plann_wirh_same_with_inner_same(self, file):
        dir1 = Dir(Path("test1"))
        dir1.inner = set((Dir(Path("test2")), File(Path("test3"))))
        dir2 = Dir(Path("test1"))
        dir2.inner = set((Dir(Path("test2")), File(Path("test3"))))
        sync = set((dir1,))
        repl = set((dir2,))
        syncr = Syncronisator(ActionOptimaser(defaultdict(set), defaultdict(set)))
        plan = syncr.get_diff(sync, repl)

        assert len(plan) == 0

    @patch("builtins.open", new_callable=mock_open, read_data="data".encode("utf-8"))
    def test_get_plann_wirh_same_with_diff_inner(self, file):
        dir1 = Dir(Path("test1"))
        dir1.inner = set((Dir(Path("test2")), File(Path("test3")), File(Path("test4"))))
        dir2 = Dir(Path("test1"))
        dir2.inner = set((Dir(Path("test2")), File(Path("test3"))))
        sync = set((dir1,))
        repl = set((dir2,))
        syncr = Syncronisator(ActionOptimaser(defaultdict(set), defaultdict(set)))
        plan = syncr.get_diff(sync, repl)

        assert len(plan) == 1
        assert isinstance(plan[0], Copy)

    @patch("builtins.open", new_callable=mock_open, read_data="data".encode("utf-8"))
    def test_get_plann_wirh_same_with_diff_inner2(self, file):
        dir1 = Dir(Path("test1"))
        dir1.inner = set(
            (
                Dir(Path("test2")),
                File(Path("test3")),
            )
        )
        dir2 = Dir(Path("test1"))

        inner_d2 = Dir(Path("test2"))
        inner_d2.inner = set([File(Path("test4"))])
        dir2.inner = set((inner_d2, File(Path("test3"))))
        sync = set((dir1,))
        repl = set((dir2,))
        syncr = Syncronisator(ActionOptimaser(defaultdict(set), defaultdict(set)))
        plan = syncr.get_diff(sync, repl)

        assert len(plan) == 1
        assert isinstance(plan[0], Remove)


@patch("builtins.open", new_callable=mock_open, read_data="data".encode("utf-8"))
class TestMovementChecker:
    def test_check(self, file):
        file1 = File(Path("test1"))
        file2 = File(Path("test2"))

        assert file1._hash == file2._hash

        source = defaultdict(set)
        source[file1._hash].add(file1)

        replica = defaultdict(set)
        replica[file2._hash].add(file2)
        mc = ActionOptimaser(source, replica)

        assert mc.can_move(file1)
        assert (
            repr(mc.move_actions(file1))
            == "[Move(from=File(PosixPath('test2')), to=File(PosixPath('test1')))]"
        )

        assert not mc.can_move(file1)
