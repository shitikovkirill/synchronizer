import logging
import sys


def set_logger(filename="logs.log"):
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename=filename, level=logging.DEBUG, format=format)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    root.addHandler(handler)
