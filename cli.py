import argparse
import os
from pathlib import Path
import time
from sync.log import set_logger
from sync.main import run


def is_dir(path):
    path = Path(path)
    if path.is_dir():
        return path.absolute()
    else:
        raise argparse.ArgumentTypeError(f"dir with this name not exist: {path}")


def create_dir(path):
    path = Path(path)
    if not path.exists():
        path.mkdir()
    return path.absolute()


parser = argparse.ArgumentParser(
    prog="Sync",
    description="Sync folder",
)

parser.add_argument("source", type=is_dir)
parser.add_argument("replica", type=create_dir)
parser.add_argument("-lf", "--log_name", default="logs.log", type=str)
parser.add_argument("-i", "--interval", default=5, type=int)

args = parser.parse_args()

set_logger(filename=args.log_name)

while True:
    try:
        run(args.source, args.replica)
        time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Interrupted")
        break
