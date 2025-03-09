from .actions import Copy, Remove
from .nodes import Dir


def _get_only_dir(nodes: set):
    dirs = set(filter(lambda x: isinstance(x, Dir), nodes))
    return dirs


def plan_syncronisation(source: set, replica: set):
    plan = []

    need_remove = replica.difference(source)
    for node in need_remove:
        plan.append(Remove(node))

    need_add = source.difference(replica)
    for node in need_add:
        plan.append(Copy(node))

    source_intersection: set[Dir] = _get_only_dir(replica.intersection(source))
    replica_intersection: set[Dir] = _get_only_dir(source.intersection(replica))

    for source_node in source_intersection:
        for replica_node in replica_intersection:
            if source_node == replica_node:
                plan += plan_syncronisation(source_node.inner, replica_node.inner)

    return plan
