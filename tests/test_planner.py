from collections import defaultdict
from pathlib import Path
from sync.planner import Syncronizer
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

    @patch("builtins.open", new_callable=mock_open, read_data="data".encode("utf-8"))
    def test_plan_wirh_move_from_replica(self, file):
        file1 = File(Path("test1"))
        file2 = File(Path("test2"))
        need_add = set((file1,))
        need_remove = set((file2,))

        sync = defaultdict(set)
        sync[file1._hash].add(file1)

        repl = defaultdict(set)
        repl[file2._hash].add(file2)

        syncr = Syncronizer(sync, repl)
        plan = syncr.plan(need_remove, need_add)

        assert (
            repr(plan)
            == "[Move(from=File(PosixPath('test2')), to=File(PosixPath('test1')))]"
        )
        assert len(plan) == 1

    @patch("builtins.open", new_callable=mock_open, read_data="data".encode("utf-8"))
    def test_plan_wirh_copy_from_replica(self, file):
        file1 = File(Path("test1"))
        need_add = set((file1,))

        file2 = File(Path("test2"))

        sync = defaultdict(set)
        sync[file1._hash].add(file1)
        sync[file2._hash].add(file2)

        repl = defaultdict(set)
        repl[file2._hash].add(file2)

        syncr = Syncronizer(sync, repl)
        plan = syncr.plan(set(), need_add)

        assert (
            repr(plan)
            == "[Copy(from=File(PosixPath('test2')), to=File(PosixPath('test1')))]"
        )
        assert len(plan) == 1

    @patch("builtins.open", new_callable=mock_open, read_data="data".encode("utf-8"))
    def test_plan_wirh_copy_from_source(self, file):
        file1 = File(Path("test1"))
        need_add = set((file1,))

        sync = defaultdict(set)
        sync[file1._hash].add(file1)

        repl = defaultdict(set)

        syncr = Syncronizer(sync, repl)
        plan = syncr.plan(set(), need_add)

        assert (
            repr(plan)
            == "[Copy(from=File(PosixPath('test1')), to=File(PosixPath('test1')))]"
        )
        assert len(plan) == 1
