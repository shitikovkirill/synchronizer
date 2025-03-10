from collections import defaultdict
import logging
from sync.actions import Copy, Create, Move, Remove
from sync.nodes import Dir, File

logger = logging.getLogger(__name__)


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

    def can_be_moved_from_replica(self, source_file: File):
        return self.replica_fs[source_file._hash].difference(
            self.source_fs[source_file._hash]
        )

    def can_be_copied_from_replica(self, source_file: File):
        return self.replica_fs[source_file._hash]

    def plan(self, need_remove: set[Dir | File], need_add: set[Dir | File]):
        create_dir = []
        copied_from_replica = []
        moved_from_replica = []
        removed = []
        copy_from_source = []

        need_add_dir = filter(lambda x: isinstance(x, Dir), need_add)
        for node_dir in need_add_dir:
            create_dir.append(Create(node_dir))
            logger.info(f"Create directory: {node_dir.path}")

        need_add_file = filter(lambda x: isinstance(x, File), need_add)
        for node_file in need_add_file:
            files_for_move = self.can_be_moved_from_replica(node_file)
            files_for_copy = self.can_be_copied_from_replica(node_file)
            if files_for_move:
                exist_file = files_for_move.pop()
                moved_from_replica.append(Move(exist_file, node_file))
                self.replica_fs[node_file._hash].remove(exist_file)
                need_remove.remove(exist_file)
                logger.info(
                    f"Can be moved from replica. from={exist_file.abs_path} to={node_file.path}"
                )
            elif files_for_copy:
                exist_file = list(files_for_copy)[0]
                copied_from_replica.append(Copy(exist_file, node_file))
                logger.info(
                    f"Can be copied from replica. from={exist_file.abs_path} to={node_file.path}"
                )
            else:
                copy_from_source.append(Copy(node_file))
                logger.info(
                    f"Copy from source. from={node_file.abs_path} to={node_file.path}"
                )

        need_remove_file = filter(lambda x: isinstance(x, File), need_remove)
        for node in need_remove_file:
            removed.append(Remove(node))
            logger.info(f"Remove file. {node.abs_path}")

        need_remove_dir = filter(lambda x: isinstance(x, Dir), need_remove)
        for node in need_remove_dir:
            removed.append(Remove(node))
            logger.info(f"Remove dir. {node.abs_path}")

        return (
            create_dir
            + copied_from_replica
            + moved_from_replica
            + removed
            + copy_from_source
        )
