from collections import defaultdict
import logging
import os
from pathlib import Path
import sys

from sync.planner import get_tree_diff, Syncronizer
from sync.tree import TreeBuilder


logger = logging.getLogger(__name__)


def set_logger():
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename="logs.log", level=logging.DEBUG, format=format)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    root.addHandler(handler)


def run(sourse: Path, replica: Path):
    set_logger()
    replica.mkdir(parents=True, exist_ok=True)
    abs_pass = replica.absolute()

    logger.info("Build sourse tree")
    sourse_file_store = defaultdict(set)
    builder = TreeBuilder(sourse_file_store)

    os.chdir(sourse)
    sourse_tree = builder.build(Path("."))
    logger.debug(sourse_tree)

    logger.info("Build replica tree")

    replica_file_store = defaultdict(set)
    builder = TreeBuilder(replica_file_store)

    os.chdir(abs_pass)
    replica_tree = builder.build(Path("."))
    logger.debug(replica_tree)

    logger.info("Get tree diff")
    diff = get_tree_diff(sourse_tree, replica_tree)
    logger.debug(f"Need rm: {diff[0]}")
    logger.debug(f"Need add: {diff[1]}")

    logger.info("Run preparing plan")
    syncr = Syncronizer(sourse_file_store, replica_file_store)
    plan = syncr.plan(*diff)
    logger.debug(f"Sincronisation plan: {diff[1]}")

    for cmd in plan:
        logger.info(f"Run command {cmd}")
        cmd()
