from collections import defaultdict
from sync.actions import Copy, Create, Move, Remove
from sync.nodes import Dir, File


def _get_only_dir(nodes: set):
    dirs = set(filter(lambda x: isinstance(x, Dir), nodes))
    return dirs


def get_tree_diff(source: Dir, replica: Dir):
    all_source = source.get_all_nodes()
    all_replica = replica.get_all_nodes()

    need_remove = all_replica.difference(all_source)
    need_add = all_source.difference(all_replica)

    return need_remove, need_add


class Syncronizer:
    def __init__(
        self,
        source_file_storage: defaultdict[str, set],
        replica_file_storage: defaultdict[str, set],
    ):
        self.source_fs = source_file_storage
        self.replica_fs = replica_file_storage

    def get_files_with_same_content(self, source_file: File):
        return self.replica_fs[source_file._hash].difference(
            self.source_fs[source_file._hash]
        )

    def plan(self, need_remove: set[Dir | File], need_add: set[Dir | File]):
        plan = []
        need_add_dir = filter(lambda x: isinstance(x, Dir), need_add)
        for node_dir in need_add_dir:
            plan.append(Create(node_dir))

        need_add_file = filter(lambda x: isinstance(x, File), need_add)
        for node_file in need_add_file:
            files = self.get_files_with_same_content(node_file)
            if files:
                exist_file = files.pop()
                plan.append(Move(exist_file, node_file))
                self.replica_fs[node_file._hash].remove(exist_file)
                need_remove.remove(exist_file)
            else:
                plan.append(
                    Copy(
                        node_file,
                    )
                )

        need_remove_file = filter(lambda x: isinstance(x, File), need_remove)
        for node in need_remove_file:
            plan.append(Remove(node))

        need_remove_dir = filter(lambda x: isinstance(x, Dir), need_remove)
        for node in need_remove_dir:
            plan.append(Remove(node))

        return plan
