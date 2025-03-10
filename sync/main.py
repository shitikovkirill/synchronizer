from collections import defaultdict
import logging
import os
from pathlib import Path

from sync.planner import get_tree_diff, Syncronizer
from sync.tree import TreeBuilder


logger = logging.getLogger(__name__)


def run(sourse: Path, replica: Path):

    logger.info("Build sourse tree")
    sourse_file_store = defaultdict(set)
    builder = TreeBuilder(sourse_file_store)

    os.chdir(sourse)
    sourse_tree = builder.build(Path("."))
    logger.debug(sourse_tree)

    logger.info("Build replica tree")

    replica_file_store = defaultdict(set)
    builder = TreeBuilder(replica_file_store)

    os.chdir(replica)
    replica_tree = builder.build(Path("."))
    logger.debug(replica_tree)

    logger.info("Get tree diff")
    diff = get_tree_diff(sourse_tree, replica_tree)
    logger.debug(f"Need rm: {diff[0]}")
    logger.debug(f"Need add: {diff[1]}")

    logger.info("Run preparing plan")
    syncr = Syncronizer(sourse_file_store, replica_file_store)
    plan = syncr.plan(*diff)
    logger.debug(f"Sincronisation plan: {plan}")

    for cmd in plan:
        logger.info(f"Run command {cmd}")
        cmd()
